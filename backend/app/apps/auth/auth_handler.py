import datetime as dt
from uuid import uuid4

import jwt
from apps.auth.password_handler import PasswordEncrypt
from apps.auth.schemas import LoginResponseSchema
from apps.users.crud import User, user_manager
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from services.redis_service import redis_service
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

        tokens_response = await self.generate_tokens(user=user)
        return tokens_response

    async def generate_tokens(self, user: User) -> LoginResponseSchema:
        access_token_payload = {
            "sub": str(user.id),
            "email": user.email,
        }
        access_token = await self.generate_token(
            payload=access_token_payload, expire_minutes=self.access_token_expires
        )

        refresh_token_payload = {
            "sub": str(user.id),
            "email": user.email,
            "key": uuid4().hex,
        }

        refresh_token = await self.generate_token(
            payload=refresh_token_payload, expire_minutes=self.refresh_token_expires
        )

        await redis_service.set_cache(
            key=refresh_token_payload["key"],
            value=user.id,
            ttl=self.refresh_token_expires,
        )

        return LoginResponseSchema(
            access_token=access_token,
            refresh_token=refresh_token,
            expired_at=self.access_token_expires * 60,
        )

    async def generate_token(self, payload: dict, expire_minutes: int) -> str:
        now = dt.datetime.now()
        token_expires_at = dt.timedelta(minutes=expire_minutes)
        time_payload = {
            "exp": now + token_expires_at,
            "iat": now,
        }
        payload.update(time_payload)
        token = jwt.encode(payload, self.jwt_secret, algorithm=self.jwt_algorithm)
        return token

    async def decode_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, self.jwt_secret, [self.jwt_algorithm])
            payload["iat"] = dt.datetime.fromtimestamp(payload.get("iat") or 0)
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired"
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token"
            )

    async def get_refresh_tokens(
        self, refresh_token: str, session: AsyncSession
    ) -> LoginResponseSchema:
        payload = await self.decode_token(refresh_token)

        stored_refresh = await redis_service.get_cache(payload["key"])
        if not stored_refresh:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Token was used already"
            )
        await redis_service.delete_cache(payload["key"])
        user: User | None = await user_manager.get(
            session=session, field=User.id, field_value=int(payload["sub"])
        )
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        tokens_response = await self.generate_tokens(user=user)
        return tokens_response


auth_handler = AuthHandler()
