from contextvars import ContextVar
from typing import Optional
from glob_utils import APIClient  # type: ignore
from pydantic import Field

oauth_token: ContextVar[Optional[str]] = ContextVar("oauth_token", default=None)


class GmailAPIClient(APIClient):
    base_url: str = Field(default="https://gmail.googleapis.com")
    headers: dict[str, str] = Field(...)

    @classmethod
    def set_token(cls, token: str):
        oauth_token.set(token)

    @classmethod
    def get_token(cls) -> Optional[str]:
        return oauth_token.get()

    @classmethod
    def clear_token(cls):
        oauth_token.set(None)

    @classmethod
    def from_env(cls):
        return cls(headers={"Authorization": f"Bearer {cls.get_token()}"})


class GoogleAPIClient(APIClient):
    base_url: str = Field(default="https://www.googleapis.com")
    headers: dict[str, str] = Field(...)

    @classmethod
    def set_token(cls, token: str):
        oauth_token.set(token)

    @classmethod
    def get_token(cls) -> Optional[str]:
        return oauth_token.get()

    @classmethod
    def clear_token(cls):
        oauth_token.set(None)

    @classmethod
    def from_env(cls):
        return cls(headers={"Authorization": f"Bearer {cls.get_token()}"})
