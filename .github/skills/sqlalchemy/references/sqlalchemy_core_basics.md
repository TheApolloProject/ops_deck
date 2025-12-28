# SQLAlchemy Core Basics

SQLAlchemy Core provides a lower-level, explicit SQL construction layer.

## Tables and metadata

```python
from sqlalchemy import Table, Column, MetaData, Integer, String

metadata = MetaData()

user_table = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String, nullable=False, unique=True),
)
````

## Basic statements

```python
from sqlalchemy import select, insert, update, delete

stmt_select = select(user_table)
stmt_insert = insert(user_table).values(email="example@example.com")
stmt_update = update(user_table).where(user_table.c.id == 1).values(email="new@example.com")
stmt_delete = delete(user_table).where(user_table.c.id == 1)
```

Use Core when fine-grained SQL control is required or when the ORM is unnecessary.