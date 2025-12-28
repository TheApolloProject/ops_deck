# Migrations with Alembic

Alembic manages schema evolution for SQLAlchemy-backed projects.

## Configuration

- Point Alembic to the project models:
  - In `env.py`, import `Base` and set `target_metadata = Base.metadata`.
- Store `sqlalchemy.url` in `alembic.ini` or via environment variables.

## Generating migrations

```bash
alembic revision -m "create user table" --autogenerate
alembic upgrade head
````

Review generated migrations, especially when dropping columns or tables. Avoid guessing production history; always inspect existing schema and data.