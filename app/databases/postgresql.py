from contextlib import asynccontextmanager
from typing import TypeAlias, Any, AsyncGenerator

from sanic import Sanic
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from app.extensions import Base
from app.misc.log import log

# Type alias for the session maker, following PascalCase convention
AsyncSessionMaker: TypeAlias = async_sessionmaker[AsyncSession]


class PostgreSQL:
    """Manages PostgreSQL connection, engine, and sessions."""

    def __init__(self) -> None:
        self.engine: AsyncEngine | None = None
        self.session_maker: AsyncSessionMaker | None = None

    async def setup(self, database_uri: str, debug: bool = False) -> None:
        """Create DB engine, session maker, and tables."""
        uri = database_uri.replace("postgresql://", "postgresql+asyncpg://")
        self.engine = create_async_engine(uri, echo=debug)
        self.session_maker = async_sessionmaker(
            bind=self.engine, autoflush=False, autocommit=False
        )
        log(f"Database engine initialized: {uri}", keyword="INFO")

        # Create all tables
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        log("Database schema created.", keyword="INFO")

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, Any]:
        """Provide a transactional session."""
        if not self.session_maker:
            raise RuntimeError("Database not initialized. Call setup() first.")

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
            log("Database engine disposed.", keyword="INFO")


# A single, shared instance for the entire application
postgres_db = PostgreSQL()
