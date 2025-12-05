from fastapi import FastAPI, requests

from scalar_fastapi import get_scalar_api_reference

from apps.info.router import info_router
from apps.users.router import router_users
from settings import settings

def get_application() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        debug=settings.DEBUG,
        root_path="/api",
    )
    app.include_router(router_users, prefix="/users", tags=["Users"])

    if settings.DEBUG:
        app.include_router(info_router, prefix="/info", tags=["Info"])

    @app.get("/scalar", include_in_schema=False)
    async def scalar_html(request: requests.Request):
        return get_scalar_api_reference(
            openapi_url=request.scope.get('root_path', "") + app.openapi_url,
            title=app.title,
        )

    return app
