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

    return user
