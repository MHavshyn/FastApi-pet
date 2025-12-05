from apps.auth.password_handler import PasswordEncrypt
from apps.auth.schemas import LoginResponseSchema
from apps.users.crud import User, user_manager
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from settings import settings
from sqlalchemy.ext.asyncio import AsyncSession


class AuthHandler:
    def __init__(self):
        self.access_token_expires = settings.ACCESS_TOKEN_TIME_MINUTES
        self.refresh_token_expires = settings.REFRESH_TOKEN_TIME_MINUTES
        self.jwt_algorithm = settings.JWT_ALGORITHM
        self.jwt_secret = settings.JWT_SECRET_KEY

    async def get_login_token_pairs(
        self, session: AsyncSession, data: OAuth2PasswordRequestForm
    ) -> LoginResponseSchema:
        user: User | None = await user_manager.get(
            session=session, field=User.email, field_value=data.username
        )
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User with given email not found",
            )
        is_valid_password = await PasswordEncrypt.verify_password(
            plain_password=data.password, hashed_password=user.hashed_password
        )
        if not is_valid_password:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Invalid password"
            )

        return LoginResponseSchema(
            access_token="access_token",
            refresh_token="refresh_token",
            expired_at=5,
        )


auth_handler = AuthHandler()
