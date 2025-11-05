# app/repositories/__init__.py
import math
from typing import Generic, TypeVar, Type, Optional, List, Any, Dict
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, update
from sqlalchemy.inspection import inspect

from app.models.base import Base

# --- Generic Type Variables ---
ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


# --- Standardized Pagination Result Schema ---
class PaginationResult(BaseModel, Generic[ModelType]):
    """Standardized schema for paginated query results."""
    items: List[ModelType]
    total_items: int
    total_pages: int
    current_page: int
    page_size: int


# --- The New BaseRepository ---
class BaseRepository(Generic[ModelType]):
    """
    A generic, powerful, and best-practice oriented repository.

    Handles soft-deletes, pagination, and dynamic filtering/sorting.
    It operates within a given session and never commits.
    """

    def __init__(self, model: Type[ModelType], session: AsyncSession):
        """
        Initializes the repository with the SQLAlchemy model and a session.

        :param model: The SQLAlchemy model class.
        :param session: The SQLAlchemy AsyncSession for this request.
        """
        self.model = model
        self.session = session
        # Inspect the model to find the name of the primary key column
        self.pk_name = inspect(self.model).primary_key[0].name

    def _apply_filters_and_sort(
        self,
        stmt,
        filters: Optional[Dict[str, Any]] = None,
        sort_by: Optional[List[str]] = None,
        include_deleted: bool = False
    ):
        """Applies filtering, sorting, and soft-delete logic to a statement."""
        # 1. Apply soft-delete filter by default
        if hasattr(self.model, "is_deleted") and not include_deleted:
            stmt = stmt.where(self.model.is_deleted == False)

        # 2. Apply dynamic filters
        if filters:
            for field, value in filters.items():
                if hasattr(self.model, field):
                    stmt = stmt.where(getattr(self.model, field) == value)

        # 3. Apply dynamic sorting
        if sort_by:
            for sort_field in sort_by:
                direction = "desc" if sort_field.endswith("_desc") else "asc"
                field_name = sort_field.removesuffix("_desc").removesuffix("_asc")
                if hasattr(self.model, field_name):
                    column = getattr(self.model, field_name)
                    stmt = stmt.order_by(getattr(column, direction)())
        return stmt

    async def get_by_id(self, record_id: Any, include_deleted: bool = False) -> Optional[ModelType]:
        """Gets a single record by its primary key."""
        pk_column = getattr(self.model, self.pk_name)
        query = select(self.model).where(pk_column == record_id)
        
        # Apply soft-delete logic only if the model supports it
        if hasattr(self.model, "is_deleted") and not include_deleted:
            query = query.where(self.model.is_deleted == False)
            
        result = await self.session.execute(query)
        return result.scalars().first()

    async def get_many(
        self,
        *,
        filters: Optional[Dict[str, Any]] = None,
        sort_by: Optional[List[str]] = None,
        skip: int = 0,
        limit: int = 100,
        include_deleted: bool = False
    ) -> List[ModelType]:
        """Gets multiple records with filtering, sorting, and limit/offset."""
        stmt = self._apply_filters_and_sort(select(self.model), filters, sort_by, include_deleted)
        stmt = stmt.offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_paginated(
        self,
        *,
        page: int = 1,
        page_size: int = 10,
        filters: Optional[Dict[str, Any]] = None,
        sort_by: Optional[List[str]] = None,
        include_deleted: bool = False,
    ) -> PaginationResult[ModelType]:
        """Gets a paginated list of records."""
        if page < 1: page = 1
        if page_size < 1: page_size = 10

        # Create and apply filters to the count query
        count_stmt = self._apply_filters_and_sort(
            select(func.count()).select_from(self.model),
            filters,
            include_deleted=include_deleted
        )
        total_items = (await self.session.execute(count_stmt)).scalar_one()

        # Create and apply filters/sort to the data query
        data_stmt = self._apply_filters_and_sort(
            select(self.model),
            filters,
            sort_by,
            include_deleted
        )
        data_stmt = data_stmt.offset((page - 1) * page_size).limit(page_size)
        result = await self.session.execute(data_stmt)
        items = list(result.scalars().all())

        return PaginationResult(
            items=items,
            total_items=total_items,
            total_pages=math.ceil(total_items / page_size) if total_items > 0 else 0,
            current_page=page,
            page_size=page_size,
        )

    async def create(self, data: CreateSchemaType) -> ModelType:
        """Creates a new record from a Pydantic schema."""
        instance = self.model(**data.model_dump())
        self.session.add(instance)
        await self.session.flush()  # Flush to get DB-generated values like ID
        await self.session.refresh(instance) # Refresh to load all columns
        return instance

    async def update(self, record_id: Any, data: UpdateSchemaType) -> Optional[ModelType]:
        """Updates an existing record from a Pydantic schema."""
        instance = await self.get_by_id(record_id)
        if instance:
            # Use exclude_unset to only update fields that were provided in the request
            update_data = data.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(instance, key, value)
            self.session.add(instance)
            await self.session.flush()
            await self.session.refresh(instance)
        return instance

    async def delete(self, record_id: Any) -> bool:
        """Performs a hard delete of a record."""
        instance = await self.get_by_id(record_id)
        if instance:
            await self.session.delete(instance)
            await self.session.flush()
            return True
        return False

    async def soft_delete(self, record_id: Any) -> bool:
        """
        Performs a soft delete by setting `is_deleted = True`.
        Assumes the model has an `is_deleted` boolean field.
        This is more efficient as it performs a direct UPDATE without a SELECT.
        """
        if not hasattr(self.model, "is_deleted"):
            raise AttributeError(f"Model {self.model.__name__} does not have 'is_deleted' attribute.")

        pk_column = getattr(self.model, self.pk_name)
        stmt = (
            update(self.model)
            .where(pk_column == record_id)
            .where(self.model.is_deleted == False)
            .values(is_deleted=True)
        )
        result = await self.session.execute(stmt)

        if result.rowcount > 0:
            await self.session.flush()
            return True
        return False