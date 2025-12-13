"""Alembic environment configuration"""
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context
import os
from dotenv import load_dotenv
import sys
from pathlib import Path

# Load environment variables from .env file
load_dotenv()

# Add backend/src to Python path for imports
backend_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(backend_path))

# This is the Alembic Config object
config = context.config

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Get database URL from environment
database_url = os.getenv('DATABASE_URL', 'postgresql://localhost/auth_dev')

# For Alembic (synchronous migrations), convert postgresql+asyncpg:// to postgresql://
# because Alembic runs synchronously and needs the synchronous driver (psycopg or psycopg2)
if database_url.startswith('postgresql+asyncpg://'):
    database_url = database_url.replace('postgresql+asyncpg://', 'postgresql://', 1)

config.set_main_option('sqlalchemy.url', database_url)

# Model's MetaData object for 'autogenerate' support
try:
    from models.database import Base
    target_metadata = Base.metadata
except ImportError:
    # If imports fail (e.g., missing dependencies), use None
    # Migrations will still work, just without autogenerate
    target_metadata = None


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well. By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = os.getenv(
        'DATABASE_URL',
        'postgresql://localhost/auth_dev'
    )

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
