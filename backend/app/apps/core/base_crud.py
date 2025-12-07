from abc import ABC, abstractmethod
from typing import Any, Optional

from apps.core.base_models import Base
from fastapi import HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select, update
from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute


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
            raise HTTPException(
                detail=f"Error has occurred while creating {self.model} instance with {kwargs}, {e=}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    async def get(
        self, *, session: AsyncSession, field_value: Any, field: InstrumentedAttribute
    ) -> Optional[Base]:
        query = select(self.model).filter(field == field_value)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    async def patch(
        self,
        instance_id: int,
        session: AsyncSession,
        data_to_patch: BaseModel,
        exclude_unset: bool = True,
    ) -> Base:
        query = (
            select(self.model)
            .filter(self.model.id == instance_id)
            .with_for_update(nowait=True)
        )
        try:
            result = await session.execute(query)
            item = result.scalar_one_or_none()
        except DBAPIError:
            raise HTTPException(
                detail="Row locked, try again later", status_code=status.HTTP_423_LOCKED
            )

        if not item:
            raise HTTPException(
                detail=f"Item with id {instance_id} not found",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        data_for_updating: dict = data_to_patch.model_dump(
            exclude={"id"}, exclude_unset=exclude_unset
        )
        if not data_for_updating:
            return item
        query = (
            update(self.model)
            .where(self.model.id == instance_id)
            .values(**data_for_updating)
        )
        await session.execute(query)
        await session.commit()
        return item
