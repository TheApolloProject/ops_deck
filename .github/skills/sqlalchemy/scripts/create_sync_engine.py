from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Generator, Optional

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker


@dataclass
class DatabaseSettings:
    """Database connection configuration."""

    url: str = os.getenv("DATABASE_URL", "sqlite:///./app.db")
    echo: bool = bool(int(os.getenv("SQLALCHEMY_ECHO", "0")))
    future: bool = True


def get_engine(settings: Optional[DatabaseSettings] = None) -> Engine:
    """Create and return a SQLAlchemy Engine."""
    if settings is None:
        settings = DatabaseSettings()
    engine = create_engine(settings.url, echo=settings.echo, future=settings.future)
    return engine


def get_session_factory(engine: Optional[Engine] = None) -> sessionmaker[Session]:
    """Create a sessionmaker bound to the given Engine."""
    if engine is None:
        engine = get_engine()
    return sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)


def get_session(
    session_factory: Optional[sessionmaker[Session]] = None,
) -> Generator[Session, None, None]:
    """Context-managed generator for use in scripts.

    Example:
        with next(get_session()) as session:
            ...
    """
    if session_factory is None:
        session_factory = get_session_factory()
    session: Session = session_factory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    engine = get_engine()
    print(f"Created sync engine for URL: {engine.url}")
