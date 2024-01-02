from fastapi import FastAPI
from starlette.types import Receive, Scope, Send


class HSTSMiddleware:
    """HTTP Strict Transport Security middleware."""

    def __init__(
        self, app: FastAPI, max_age: int = 31536000, include_subdomains: bool = True
    ):
        self.app = app
        self.max_age = max_age
        self.include_subdomains = include_subdomains

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["scheme"] == "http":
            scope["scheme"] = "https"
            return await self.app(scope, receive, send)
        return await self.app(scope, receive, send)
