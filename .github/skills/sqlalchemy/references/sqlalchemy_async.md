# SQLAlchemy Async Usage

SQLAlchemy 2.x includes robust async support via `AsyncEngine` and `AsyncSession`.

## Engine and session

```python
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

engine = create_async_engine("sqlite+aiosqlite:///./app.db", echo=True)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)
````

## Using AsyncSession

```python
from sqlalchemy import select

async def get_user_by_email(email: str) -> User | None:
    async with AsyncSessionLocal() as session:
        stmt = select(User).where(User.email == email)
        result = await session.scalar(stmt)
        return result
```

Async patterns mirror sync usage but rely on `async with`, `await session.execute()`, and `await session.commit()`.