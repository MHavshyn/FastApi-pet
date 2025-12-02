import socket

from fastapi import APIRouter
from settings import settings

info_router = APIRouter()


@info_router.get("/backend")
async def get_backend_info():
    """Get current backend info"""
    return {"backend": socket.gethostname()}


@info_router.get("/database")
async def get_database_info():
    """Get current database info"""
    return {"database_url": settings.DATABASE_ASYNC_URL}
