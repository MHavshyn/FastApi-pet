from abc import ABC, abstractmethod

from sqlalchemy import select
from sqlalchemy.orm import InstrumentedAttribute

from apps.core.base_models import Base
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, Any
from fastapi import HTTPException, status

class BaseCRUDManager(ABC):
    model: type[Base] = None

    @abstractmethod
    def __init__(self):
        pass

    async def create(self, *, session: AsyncSession, **kwargs) -> Optional[Base]:
       instance = self.model(**kwargs)
       session.add(instance)
       try:
           await session.commit()
           return instance
       except Exception as e:
           await session.rollback()
           raise HTTPException(detail=f"Error has occurred while creating {self.model} instance with {kwargs}, {e=}", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def get(self, *, session: AsyncSession, field_value: Any, field: InstrumentedAttribute) ->Optional[Base]:
        query = select(self.model).filter(field == field_value)
        result = await session.execute(query)
        return result.scalar_one_or_none()
