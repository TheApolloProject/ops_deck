from __future__ import annotations

import os
from dataclasses import dataclass
from typing import AsyncGenerator, Optional

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


@dataclass
class AsyncDatabaseSettings:
    """Async database connection configuration."""

    url: str = os.getenv("ASYNC_DATABASE_URL", "sqlite+aiosqlite:///./app.db")
    echo: bool = bool(int(os.getenv("SQLALCHEMY_ECHO", "0")))


def get_async_engine(settings: Optional[AsyncDatabaseSettings] = None) -> AsyncEngine:
    """Create and return an AsyncEngine."""
    if settings is None:
        settings = AsyncDatabaseSettings()
    engine = create_async_engine(settings.url, echo=settings.echo)
    return engine


def get_async_session_factory(
    engine: Optional[AsyncEngine] = None,
) -> async_sessionmaker[AsyncSession]:
    """Create an async_sessionmaker bound to the given AsyncEngine."""
    if engine is None:
        engine = get_async_engine()
    return async_sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)


async def get_async_session(
    session_factory: Optional[async_sessionmaker[AsyncSession]] = None,
) -> AsyncGenerator[AsyncSession, None]:
    """Async context-managed generator for use in async scripts."""
    if session_factory is None:
        session_factory = get_async_session_factory()
    async with session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


if __name__ == "__main__":
    engine = get_async_engine()
    print(f"Created async engine for URL: {engine.url}")
