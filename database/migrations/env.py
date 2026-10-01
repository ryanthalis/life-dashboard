import asyncio
import os
import re
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool, text
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from server.config import get_settings
from server.models import Base


config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

database_url = get_settings().database_url.render_as_string(hide_password=False)
config.set_main_option("sqlalchemy.url", database_url.replace("%", "%%"))
target_metadata = Base.metadata

MIGRATION_SCHEMA = os.getenv("LIFE_DB_MIGRATION_SCHEMA")
if MIGRATION_SCHEMA and not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", MIGRATION_SCHEMA):
    raise ValueError("LIFE_DB_MIGRATION_SCHEMA must be a PostgreSQL identifier")


def include_object(
    object_: object,
    name: str | None,
    type_: str,
    reflected: bool,
    compare_to: object | None,
) -> bool:
    return not (type_ == "table" and name == "alembic_version")


def run_migrations_offline() -> None:
    context.configure(
        url=config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        include_object=include_object,
        version_table_schema=MIGRATION_SCHEMA,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        include_object=include_object,
        version_table_schema=MIGRATION_SCHEMA,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        if MIGRATION_SCHEMA:
            await connection.execute(
                text(f'SET search_path TO "{MIGRATION_SCHEMA}", public')
            )
            await connection.commit()
            connection.sync_connection.dialect.default_schema_name = MIGRATION_SCHEMA
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_async_migrations())
