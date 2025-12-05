from fastapi import APIRouter, status, Depends

from apps.auth.password_handler import PasswordEncrypt
from apps.users.schemas import RegisterUserSchema, RegisteredUserSchema
from apps.core.dependencies import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from .crud import user_manager

router_users = APIRouter()


@router_users.post("/create", status_code=status.HTTP_201_CREATED)
async def create_users(new_uses: RegisterUserSchema, session: AsyncSession = Depends(get_async_session)) -> RegisteredUserSchema:
    created_user = await user_manager.create_user(new_uses, session)
    return created_user

