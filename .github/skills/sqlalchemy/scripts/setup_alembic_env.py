from __future__ import annotations

from logging.config import fileConfig
from typing import Any

from alembic import context
from sqlalchemy import engine_from_config, pool


def get_target_metadata() -> Any:
    """Return metadata object for Alembic to use.

    Import the project's Base here to avoid circular imports in env.py.
    """
    from myapp.db.models import Base  # Replace with real location

    return Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    config = context.config
    if config.config_file_name is not None:
        fileConfig(config.config_file_name)

    url = config.get_main_option("sqlalchemy.url")
    target_metadata = get_target_metadata()

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    config = context.config
    if config.config_file_name is not None:
        fileConfig(config.config_file_name)

    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    target_metadata = get_target_metadata()

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata, compare_type=True)

        with context.begin_transaction():
            context.run_migrations()


def run() -> None:
    """Entry point that chooses offline or online mode."""
    if context.is_offline_mode():
        run_migrations_offline()
    else:
        run_migrations_online()
