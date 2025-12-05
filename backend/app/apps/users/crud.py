from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from apps.core.base_crud import BaseCRUDManager
from .models import User
from .schemas import RegisterUserSchema
from apps.auth.password_handler import PasswordEncrypt


class UserCRUDManager(BaseCRUDManager):
    def __init__(self):
        self.model = User

    async def create_user(self, new_user: RegisterUserSchema, session: AsyncSession) -> User:
        maybe_user = await self.get(session=session, field=self.model.email, field_value=new_user.email)
        if maybe_user:
            raise HTTPException(detail="User with this email already exists", status_code=status.HTTP_409_CONFLICT)

        hashed_password = await PasswordEncrypt.get_password_hash(new_user.password)
        user = await self.create(
            session=session,
            name=new_user.name,
            email=new_user.email,
            hashed_password=hashed_password
        )
        return user


user_manager = UserCRUDManager()
