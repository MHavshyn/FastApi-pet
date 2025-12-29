from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from apps.auth.router import router_auth
from apps.info.router import info_router
from apps.products.router import router_categories, router_orders, router_products
from apps.users.router import router_users
from fastapi import FastAPI, requests
from fastapi.responses import ORJSONResponse
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from scalar_fastapi import get_scalar_api_reference
from services.redis_service import redis_service
from services.sentry_service import init_sentry
from settings import settings

init_sentry()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    redis = redis_service.redis
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield
    await redis.close()
    await redis.connection_pool.disconnect()


def get_application() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        debug=settings.DEBUG,
        root_path="/api",
        default_response_class=ORJSONResponse,
        lifespan=lifespan,
    )
    app.include_router(router_auth, prefix="/auth", tags=["auth"])
    app.include_router(router_users, prefix="/users", tags=["Users"])
    app.include_router(router_categories, prefix="/categories", tags=["Categories"])
    app.include_router(router_products, prefix="/products", tags=["Products"])
    app.include_router(router_orders, prefix="/orders", tags=["Oeders"])

    if settings.DEBUG:
        app.include_router(info_router, prefix="/info", tags=["Info"])

    @app.get("/scalar", include_in_schema=False)
    async def scalar_html(request: requests.Request):
        return get_scalar_api_reference(
            openapi_url=request.scope.get("root_path", "") + app.openapi_url,
            title=app.title,
        )

    return app
