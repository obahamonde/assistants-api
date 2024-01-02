import asyncio
import base64

from bs4 import BeautifulSoup
from fastapi import Request
from httpx import AsyncClient
from pydantic import BaseModel, Field  # pylint: disable=no-name-in-module

from ...schemas.functions import OpenAIFunction
from ._client import APIClient, GmailAPIClient

SCRAPPING_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
}


class GoogleAPIClient(APIClient):
    base_url: str = Field(default="https://www.googleapis.com")
    headers: dict[str, str] = Field(...)

    @classmethod
    def from_env(cls, request: Request):
        token = request.headers.get("Authorization")
        assert token is not None, "Authorization header is missing"
        return cls(headers={"Authorization": token})


class GmailEmail(BaseModel):
    id: str
    date: str
    subject: str
    body: str


class SendEmailResponse(BaseModel):
    message: str


class GetEmailsResponse(BaseModel):
    emails: list[GmailEmail]


class GmailSendFunction(OpenAIFunction[SendEmailResponse]):
    """
    Send emails using Gmail
    """

    to: str = Field(...)
    subject: str = Field(...)
    body: str = Field(...)

    async def run(self):
        client = GmailAPIClient.from_env()
        client.post(
            "/gmail/v1/users/me/messages/send",
            json={
                "raw": base64.urlsafe_b64encode(
                    f"""From: "OpenAI" <{client.email}>
To: {self.to}
Subject: {self.subject}

{self.body}""".encode()
                ).decode(),
            },
        )
        return SendEmailResponse(message="Email sent")


class GoogleSearchResult(BaseModel):
    title: str
    url: str
    content: str


class GoogleSearchFunction(OpenAIFunction[list[GoogleSearchResult]]):
    """
    Search Google
    """

    query: str = Field(...)

    async def run(self):
        async with AsyncClient() as client:
            response = await client.get(
                "https://www.google.com/search",
                params={"q": self.query},
                headers=SCRAPPING_HEADERS,
            )
            soup = BeautifulSoup(response.text, "lxml")
            results = soup.find_all("div", class_="yuRUbf")
            urls = [result.a["href"] for result in results]
            contents = await asyncio.gather(
                *[self.get_content(url, client) for url in urls]
            )
            return [
                GoogleSearchResult(
                    title=result.h3.text,
                    url=result.a["href"],
                    content=content,
                )
                for result, content in zip(results, contents)
            ]

    async def get_content(self, url: str, session: AsyncClient) -> str:
        response = await session.get(url, headers=SCRAPPING_HEADERS)
        soup = BeautifulSoup(response.text, "lxml")
        return soup.get_text()


class SiteMapResponse(BaseModel):
    url: str = Field(..., description="URL of the sitemap")
    pages: int = Field(..., description="Number of pages in the sitemap")


class Website(BaseModel):
    url: str
    content: str


class SiteMapFunction(OpenAIFunction[list[str]]):
    """
    This functions returns all the URLs in a sitemap
    """

    base_url: str
    child_urls: list[str] = Field(default_factory=list)

    async def _fetch_all_urls_recursively(
        self, url: str, session: AsyncClient
    ) -> list[str]:
        self.child_urls.extend(
            [
                a["href"]
                for a in BeautifulSoup(
                    (await session.get(url, headers=SCRAPPING_HEADERS)).text
                ).find_all("a", href=True)
            ]
        )
        await asyncio.gather(
            *[
                self._fetch_all_urls_recursively(child_url, session)
                for child_url in self.child_urls
            ]
        )
        return self.child_urls

    async def run(self):
        async with AsyncClient() as session:
            return await self._fetch_all_urls_recursively(self.base_url, session)
