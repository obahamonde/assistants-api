from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .controllers import setup_ai_routes, setup_routes


def create_app() -> FastAPI:
    """
    Creates the FastAPI app.
    """
    app = FastAPI(title="AI Assistants API", version="0.0.1", debug=True)
    app.include_router(setup_routes())
    app.include_router(setup_ai_routes())
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )

    return app


__all__ = ["create_app"]
