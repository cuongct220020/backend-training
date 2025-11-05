from contextlib import asynccontextmanager
from typing import TypeAlias, Any, AsyncGenerator

# from sanic import Sanic
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from app.models.base import Base
from app.exceptions import ServerError
from app.utils.logger_utils import get_logger

logger = get_logger(__name__)

# Type alias for the session maker, following PascalCase convention
AsyncSessionMaker: TypeAlias = async_sessionmaker[AsyncSession]


class PostgreSQLManager:
    """Manages PostgreSQL connection, engine, and sessions."""

    def __init__(self) -> None:
        self.engine: AsyncEngine | None = None
        self.session_maker: AsyncSessionMaker | None = None

    async def setup(self, database_uri: str, debug: bool = False) -> None:
        """Create DB engine, session maker"""
        self.engine = create_async_engine(database_uri, echo=debug)
        self.session_maker = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False
        )
        logger.info(f"Database engine initialized: {database_uri}")

    async def create_tables(self) -> None:
        """Creates all database tables defined in the models."""
        if not self.engine:
            raise ServerError("Database engine not initialized. Call setup() first.")

        logger.info("Initializing database tables...")
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables initialized successfully.")

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, Any]:
        """Provide a transactional session."""
        if not self.session_maker:
            raise ServerError("Database not initialized. Call setup() first.")

        session = self.session_maker()
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    async def dispose(self) -> None:
        """Dispose of the database engine and close all connections."""
        if self.engine:
            await self.engine.dispose()
            logger.info("Database engine disposed.")


# A single, shared instance for the entire application
postgres_db = PostgreSQLManager()
