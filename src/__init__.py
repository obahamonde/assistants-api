from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from .controllers import setup_ai_routes, setup_routes


def create_app() -> FastAPI:
    app = FastAPI(title="AI Assistants API", version="0.0.1", debug=True)

    # Setup API routes
    app.include_router(setup_routes())
    app.include_router(setup_ai_routes())

    # Setup static files
    app.mount("/static", StaticFiles(directory="src/static"), name="static")

    # Fallback route to serve the SPA
    @app.get("/", response_class=HTMLResponse)
    async def _():
        return open("src/static/index.html").read()

    return app


__all__ = ["create_app"]
