# app/repositories/__init__.py
from typing import Generic, TypeVar, Type, Optional, List, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """Generic repository initialized with a session for a single request."""

    def __init__(self, model: Type[ModelType], session: AsyncSession):
        self.model = model
        self.session = session

    async def create(self, data: dict) -> ModelType:
        instance = self.model(**data)
        self.session.add(instance)
        return instance

    async def get_by_id(self, record_id: Any) -> Optional[ModelType]:
        return await self.session.get(self.model, record_id)

    async def get_all(self, *, skip: int = 0, limit: int = 100) -> List[ModelType]:
        query = select(self.model).offset(skip).limit(limit)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def update(self, record_id: Any, data: dict) -> Optional[ModelType]:
        instance = await self.get_by_id(record_id)
        if instance:
            for key, value in data.items():
                setattr(instance, key, value)
            self.session.add(instance)
        return instance

    async def delete(self, record_id: Any) -> bool:
        instance = await self.get_by_id(record_id)
        if instance:
            await self.session.delete(instance)
            return True
        return False