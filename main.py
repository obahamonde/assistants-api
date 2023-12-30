from typing import Any, Awaitable, Callable

from dotenv import load_dotenv
from fastapi import Request, Response
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from src import create_app
from src.resources.functions import OpenAIFunction
from src.services.apps import GmailSendFunction, GoogleSearchFunction
from src.services.apps.google_gmail import (
    GmailAPIClient,
    GoogleAPIClient,
    SiteMapFunction,
)

load_dotenv()

app = create_app()


@app.get("/api/function")
def list_functions():
    return [func.definition() for func in OpenAIFunction.__subclasses__()]


@app.post("/api/function")
async def function_call(text: str):
    return await OpenAIFunction.exec(text)  # type: ignore


@app.get("/api/sitemap")
async def sitemap_xml(url: str):
    func = SiteMapFunction(base_url=url)
    return await func()
