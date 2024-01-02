from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

from .controllers import HSTSMiddleware, setup_ai_routes, setup_routes


def create_app() -> FastAPI:
    app = FastAPI(
        title="Assistants API",
        description="Assistants API",
        version="0.1.0",
    )
    app.mount("/static", StaticFiles(directory="static"), name="static")
    app.mount("/openai", StaticFiles(directory="docs"), name="openai")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    # app.add_middleware(HSTSMiddleware)
    app.include_router(setup_routes())
    app.include_router(setup_ai_routes())

    @app.get("/openai")
    async def _():
        return RedirectResponse("/openai/index.html")

    @app.get("/sitemap.xml")
    async def _():
        return FileResponse("docs/sitemap.xml")

    @app.get("/")
    async def _():
        return FileResponse("static/index.html")

    return app
