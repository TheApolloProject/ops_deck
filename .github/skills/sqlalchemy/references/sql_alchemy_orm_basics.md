# SQLAlchemy ORM Basics

This reference summarises the core patterns for using SQLAlchemy's ORM in 2.x-style code.

## Declarative base and models

Use a typed base class:

```python
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass
````

Define models with `Mapped[...]` and `mapped_column()`:

```python
from sqlalchemy import String, Integer, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
```

## Simple relationships

One-to-many:

```python
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class Post(Base):
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="posts")


User.posts = relationship("Post", back_populates="user")
```

Use these patterns as the default for ORM-centric projects.