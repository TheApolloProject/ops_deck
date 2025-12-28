from __future__ import annotations

from typing import AsyncGenerator, Generator

from fastapi import Depends  # noqa: F401  # used in FastAPI routes
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

# Import or construct these factories from your engine setup modules.
# For example:
# from .create_sync_engine import get_engine, get_session_factory
# from .create_async_engine import get_async_engine, get_async_session_factory

SyncSessionFactory = sessionmaker[Session]
AsyncSessionFactory = async_sessionmaker[AsyncSession]

sync_session_factory: SyncSessionFactory
async_session_factory: AsyncSessionFactory


def configure_sync_session_factory(factory: SyncSessionFactory) -> None:
    """Wire a sync session factory at application startup."""
    global sync_session_factory
    sync_session_factory = factory


def configure_async_session_factory(factory: AsyncSessionFactory) -> None:
    """Wire an async session factory at application startup."""
    global async_session_factory
    async_session_factory = factory


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency that yields a sync Session."""
    session: Session = sync_session_factory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency that yields an AsyncSession."""
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
