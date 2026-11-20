from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from sqlmodel import SQLModel

from alembic import context
from noor_foods_api import models  # noqa: F401
from noor_foods_api.config import get_settings

config = context.config
config.set_main_option("sqlalchemy.url", get_settings().database_url)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


target_metadata = SQLModel.metadata
managed_tables = {"rider_shifts"}


def include_name(name: str, type_: str, parent_names: dict[str, str]) -> bool:
    """Only compare tables represented by this application models."""
    if type_ == "table":
        return name in managed_tables
    return True


def include_object(
    object_: object,
    name: str,
    type_: str,
    reflected: bool,
    compare_to: object | None,
) -> bool:
    """Exclude metadata-only foreign-key reference tables from migrations."""
    if type_ == "table":
        return name in managed_tables
    return True


def run_migrations_offline() -> None:
    """Generate SQL without opening a database connection."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        include_name=include_name,
        include_object=include_object,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations against the configured database."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_name=include_name,
            include_object=include_object,
            # Existing tables have comments that the models do not repeat.
            autogenerate_plugins=[
                "alembic.autogenerate.*",
                "~alembic.autogenerate.comments",
            ],
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
