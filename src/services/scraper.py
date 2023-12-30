import asyncio
from typing import Optional

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
    "tel:",
    "javascript:",
    "mailto:",
)


class IngestWebsite(PineCone):
    urls: Optional[list[str]] = Field(default_factory=list)

    @robust
    async def sitemap(self, url: str, session: AsyncClient) -> list[str]:
        if self.urls is None:
            self.urls = []
        if not url.endswith("xml"):
            url = f"{url.rstrip('/')}/sitemap.xml"
            response = await session.get(url)
            text = response.text
            soup = BeautifulSoup(text, features="xml")
            for loc in soup.findAll("loc"):
                if loc.text.endswith(BAD_EXT) or (loc.text in self.urls):
                    continue
                self.urls.append(loc.text)
            for nested_sitemap in soup.find_all("sitemap"):
                self.urls.extend(await self.sitemap(nested_sitemap.loc.text, session))
        return self.urls

    @robust
    async def scrape(self, url: str, session: AsyncClient) -> list[str]:
        if self.urls is None:
            self.urls = []
        response = await session.get(url)
        text = response.text
        soup = BeautifulSoup(text, features="xml")
        for link in soup.find_all("a", href=True):
            url_ = link.get("href")
            if url_.endswith(BAD_EXT) or (url_ in self.urls):
                continue
            if url_.startswith("/"):
                url_ = f"{url.rstrip('/')}{url_}"
            self.urls.append(url_)
        for inner_url in self.urls:
            await self.scrape(inner_url, session)
        return self.urls

    @robust
    async def run(self, url: str) -> list[str]:
        async with AsyncClient(headers=HEADERS) as session:
            _url = url + "/sitemap.xml"
            response = await session.get(_url)
            if response.status_code == 200:
                return await self.sitemap(url, session)
            return await self.scrape(url, session)

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
    async def pipeline(
        self,
        url: str,
        session: AsyncClient,
        chunk_size: int = 32,
    ):
        urls = await self.run(url)
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
        if self.urls:
            return self.urls
        return ["No urls found"]


class IngestSiteMap(OpenAIFunction[list[str]]):
    """Iterates over all the nested urls or sitemaps of a website and ingests the text into a knowledge base."""

    url: str = Field(..., description="The base url of the website to be ingested")
    namespace: str = Field(
        ...,
        description="The name of the pinecone collection where the embeddings will be stored",
    )

    async def run(self):
        async with AsyncClient(headers=HEADERS) as session:
            return await IngestWebsite(namespace=self.namespace).pipeline(
                self.url, session
            )
