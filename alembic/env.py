from logging.config import fileConfig
from pathlib import Path
import os

from alembic import context
from sqlalchemy import create_engine, pool
from dotenv import load_dotenv

# ==========================
# Load .env
# ==========================

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL is None:
    raise ValueError("DATABASE_URL not found.")

# ==========================
# Alembic Config
# ==========================

config = context.config
config.set_main_option("sqlalchemy.url", DATABASE_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ==========================
# Import Models
# ==========================

from backend.database import Base
from backend.models.document import Document

target_metadata = Base.metadata


# ==========================
# Offline
# ==========================

def run_migrations_offline():

    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


# ==========================
# Online
# ==========================

def run_migrations_online():

    connectable = create_engine(
        DATABASE_URL,
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:

        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()