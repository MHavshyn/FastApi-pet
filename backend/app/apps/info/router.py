import socket
from asyncio import sleep
from uuid import uuid4

from fastapi import APIRouter, File, UploadFile
from fastapi_cache.decorator import cache
from settings import settings
from storage.s3 import s3_storage

from .schemas import BaseBackendInfoSchema, DatabaseInfoSchema

info_router = APIRouter()


@info_router.get("/backend")
async def get_backend_info() -> BaseBackendInfoSchema:
    """Get current backend info"""
    # logging.info("info1", extra={"info": "info1"})
    # get_betterstack_logger.info("error1", extra={"info": "info1"})
    # get_betterstack_logger.error("error2", extra={"info": "info2"})
    return BaseBackendInfoSchema(backend=socket.gethostname())


@info_router.get("/database")
async def get_database_info() -> DatabaseInfoSchema:
    """Get current database info"""
    return DatabaseInfoSchema(database_url=settings.DATABASE_ASYNC_URL)


@info_router.get("/redis")
@cache(expire=30, namespace="params")
async def heavy_endpoint(some_param: str) -> dict:
    await sleep(5)
    return {"some_param": some_param * 2}


@info_router.post("/test-upload-files")
async def upload_files(files: list[UploadFile] = File(...)) -> dict:
    uuid_id = uuid4()
    urls = await s3_storage.upload_files(files, uuid_id)
    return {"urls": urls}


# @info_router.get("/cicd-test")
# async def cicd() -> dict:
#     return {"result": "OK"}
