from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.core.config import Settings

settings = Settings()

def get_app() -> FastAPI:


    app = FastAPI(**settings.fastapi_kwargs)
    app.mount("/static", StaticFiles(directory=settings.STATIC_DIR), name="static")
    # app.include_router(router)

    return app


app = get_app()