# SQLAlchemy + FastAPI Integration

FastAPI pairs naturally with SQLAlchemy when sessions are provided as dependencies.

## Sync example

```python
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from .db import SessionLocal
from . import models

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
````

## Async example

```python
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from .db import AsyncSessionLocal  # async_sessionmaker

async def get_async_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
```

Use these as reference patterns for building CRUD endpoints that accept a session dependency.