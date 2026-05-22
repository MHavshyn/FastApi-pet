from apps.core.base_models import async_session_maker
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from services.redis_service import redis_service
from sqlalchemy import text

router_health = APIRouter()


@router_health.get("/health", include_in_schema=False)
async def health() -> dict:
    """Liveness probe. Returns 200 if the process is alive."""
    return {"status": "ok"}


@router_health.get("/healthz", include_in_schema=False)
async def healthz() -> dict:
    """Liveness probe. Returns 200 if the process is alive."""
    return {"status": "ok"}


@router_health.get("/ready", include_in_schema=False)
async def ready() -> JSONResponse:
    """Readiness probe. Verifies database and redis connectivity."""
    checks: dict = {"database": "ok", "redis": "ok"}
    healthy = True

    try:
        async with async_session_maker() as session:
            await session.execute(text("SELECT 1"))
    except Exception as exc:  # noqa: BLE001
        checks["database"] = f"error: {exc.__class__.__name__}"
        healthy = False

    try:
        pong = await redis_service.redis.ping()
        if not pong:
            checks["redis"] = "error: no pong"
            healthy = False
    except Exception as exc:  # noqa: BLE001
        checks["redis"] = f"error: {exc.__class__.__name__}"
        healthy = False

    status_code = status.HTTP_200_OK if healthy else status.HTTP_503_SERVICE_UNAVAILABLE
    return JSONResponse(
        status_code=status_code,
        content={"status": "ok" if healthy else "unavailable", "checks": checks},
    )
