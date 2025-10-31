from contextlib import asynccontextmanager
from typing import TypeAlias, Any, AsyncGenerator

# from sanic import Sanic
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from app.extensions import Base
from app.hooks import exceptions
from app.utils.logger_utils import get_logger
from app.models import User
# from config import PostgreSQLConfig

logger = get_logger(__name__)

# Type alias for the session maker, following PascalCase convention
AsyncSessionMaker: TypeAlias = async_sessionmaker[AsyncSession]


class PostgreSQL:
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
        """Creates the database tables."""
        if not self.engine:
            raise exceptions.ServerError("Database engine not initialized. Call setup() first.")

        async with self.engine.begin() as conn:
            # The original logic specifically targets the 'users' table.
            if User and hasattr(User, '__table__'):
                logger.info("Attempting to create 'users' table specifically...")
                # We pass a list of Table objects to create_all
                # User.__table__ is the Table object corresponding to the User model
                await conn.run_sync(Base.metadata.create_all, tables=[User.__table__])
            else:
                logger.warning("User model not found, falling back to create_all. This might fail.")
                # Fallback if User cannot be imported, which might cause an error
                await conn.run_sync(Base.metadata.create_all)

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, Any]:
        """Provide a transactional session."""
        if not self.session_maker:
            raise exceptions.ServerError("Database not initialized. Call setup() first.")

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
postgres_db = PostgreSQL()
