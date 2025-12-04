from abc import ABC, abstractmethod
from apps.core.base_models import Base
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from fastapi import HTTPException, status

class BaseCRUDManager(ABC):
    model: type[Base] = None

    @abstractmethod
    def __init__(self):
        pass

    async def create_instance(self, *, session: AsyncSession, **kwargs) -> Optional[Base]:
       instance = self.model(**kwargs)
       session.add(instance)
       try:
           await session.commit()
           return instance
       except Exception as e:
           await session.rollback()
           raise HTTPException(detail=f"Error has occurred while creating {self.model} instance with {kwargs}, {e=}", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
