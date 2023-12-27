import asyncio

from bs4 import BeautifulSoup
from glob_utils import robust  # type: ignore
from httpx import AsyncClient
from pydantic import Field  # pylint: disable=no-name-in-module

from ..controllers.ai import PineCone
from ..resources import OpenAIFunction

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
}
BAD_EXT = (
    "png",
    "jpg",
    "jpeg",
    "gif",
    "pdf",
    "doc",
    "docx",
    "ppt",
    "pptx",
    "xls",
    "xlsx",
    "zip",
    "rar",
    "gz",
    "7z",
    "exe",
    "mp3",
    "mp4",
    "avi",
    "mkv",
    "mov",
    "wmv",
    "flv",
    "swf",
)


class SiteMapService(PineCone):
    @robust
    async def sitemap(self, url: str, session: AsyncClient) -> list[str]:
        urls: list[str] = []
        if not url.endswith("xml"):
            url = f"{url.rstrip('/')}/sitemap.xml"
            response = await session.get(url)
            text = response.text
            soup = BeautifulSoup(text, features="xml")
            for loc in soup.findAll("loc"):
                if loc.text.endswith(BAD_EXT):
                    continue
                urls.append(loc.text)
            for nested_sitemap in soup.find_all("sitemap"):
                urls.extend(await self.sitemap(nested_sitemap.loc.text, session))
            return urls
        raise RuntimeError("Invalid sitemap")

    @robust
    async def fetch_website(
        self, url: str, session: AsyncClient, max_size: int = 40960
    ) -> str:
        response = await session.get(url)
        html = response.text
        truncated_html = html[:max_size]
        return BeautifulSoup(truncated_html, features="lxml").get_text(
            separator="\n", strip=True
        )

    @robust
    async def sitemap_pipeline(
        self,
        url: str,
        session: AsyncClient,
        chunk_size: int = 32,
    ):
        urls = await self.sitemap(url, session)
        while urls:
            chunk = urls[:chunk_size]
            urls = urls[chunk_size:]
            try:
                contents = await asyncio.gather(
                    *[self.fetch_website(url, session) for url in chunk]
                )
                await self.upsert(text=contents)
            except Exception as e:
                raise RuntimeError(e)
            await asyncio.sleep(0.5)


class IngestSiteMap(OpenAIFunction[None]):
    """Iterates over all the nested sitemap.xml related files, finds the loc of the content urls,
    scraps those urls and upserts the embeddings of the page content into the pinecone vector store.
    for further similarity search in order to feed a Large Language Model (LLM) with the content as a
    knowledge base.
    """

    url: str = Field(..., description="The base url of the website to be ingested")
    namespace: str = Field(
        ...,
        description="The name of the pinecone collection where the embeddings will be stored",
    )

    async def run(self):
        async with AsyncClient(headers=HEADERS) as session:
            await SiteMapService(namespace=self.namespace).sitemap_pipeline(
                self.url, session
            )
