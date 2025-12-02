from fastapi import FastAPI

from apps.info.router import info_router
from settings import settings

def get_application() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        debug=settings.DEBUG,
        root_path="/api",
    )

    if settings.DEBUG:
        app.include_router(info_router, prefix="/info", tags=["Info"])

    return app
