from enum import StrEnum
from typing import Callable

from apps.core.dependencies import get_async_session
from apps.users.crud import User, user_manager
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from .auth_handler import auth_handler


class SecurityHandler:
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


async def get_current_user(
    token: str = Depends(SecurityHandler.oauth2_scheme),
    session: AsyncSession = Depends(get_async_session),
) -> User:
    payload = await auth_handler.decode_token(token)

    user: User | None = await user_manager.get(
        session=session, field=User.id, field_value=int(payload["sub"])
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with given email not found",
        )

    if user.use_token_since and user.use_token_since > payload["iat"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User forced logout",
        )

    return user


async def get_admin_user(user: User = Depends(get_current_user)) -> User:
    if user.is_admin:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
    )


def require_permissions(required_permissions: list[StrEnum]) -> Callable:
    async def dependency(user: User = Depends(get_current_user)) -> User:
        if user.is_admin:
            return user
        user_permissions = set(user.permissions)
        require_permissions_set: set[str] = {per.value for per in required_permissions}

        if require_permissions_set.issubset(user_permissions):
            return user
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Permissions {', '.join(required_permissions)} required",
        )

    return dependency
