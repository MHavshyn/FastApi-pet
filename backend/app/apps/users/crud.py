from sqlalchemy.ext.asyncio import AsyncSession

from apps.core.base_crud import BaseCRUDManager
from .models import User
from .schemas import RegisterUserSchema
from apps.auth.password_handler import PasswordEncrypt


class UserCRUDManager(BaseCRUDManager):
    def __init__(self):
        self.model = User

    async def create_user(self, new_user: RegisterUserSchema, session: AsyncSession):
        hashed_password = await PasswordEncrypt.get_password_hash(new_user.password)
        user = await self.create_instance(
            session=session,
            name=new_user.name,
            email=new_user.email,
            hashed_password=hashed_password
        )
        return user


user_manager = UserCRUDManager()
