import socket

from fastapi import APIRouter
from settings import settings

from .schemas import BaseBackendInfoSchema, DatabaseInfoSchema

info_router = APIRouter()


@info_router.get("/backend")
async def get_backend_info() -> BaseBackendInfoSchema:
    """Get current backend info"""
    return BaseBackendInfoSchema(backend=socket.gethostname())


@info_router.get("/database")
async def get_database_info() -> DatabaseInfoSchema:
    """Get current database info"""
    return DatabaseInfoSchema(database_url=settings.DATABASE_ASYNC_URL)
