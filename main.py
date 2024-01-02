from typing import Any, Awaitable, Callable

from dotenv import load_dotenv
from fastapi import BackgroundTasks, Request, Response
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from src import create_app
from src.schemas.functions import OpenAIFunction
from src.tools.apps import GmailSendFunction, GoogleSearchFunction
from src.tools.apps.google_gmail import GmailAPIClient, GoogleAPIClient, SiteMapFunction
from src.tools.vector import PineDantic


class Text(BaseModel):
    text: str


load_dotenv()

app = create_app()


@app.get("/api/function")
def list_functions():
    return [func.definition() for func in OpenAIFunction.__subclasses__()]


@app.post("/api/function")
async def function_call(text: str):
    return await OpenAIFunction.exec(text)  # type: ignore


@app.get("/api/retrieval/{namespace}")
async def retrieval(namespace: str, text: str):
    func = PineDantic(namespace=namespace)
    return await func.query(text=text)


@app.post("/api/retrieval/{namespace}")
async def upsert(request: Text, namespace: str):
    func = PineDantic(namespace=namespace)
    return await func.upsert(text=request.text)
