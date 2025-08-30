
from __future__ import annotations

import os
import sys
from logging.config import fileConfig
from pathlib import Path

from alembic import context
from sqlalchemy import create_engine, pool
from sqlalchemy.engine.url import make_url
from sqlmodel import SQLModel

# --- Add src/ to sys.path so imports work when running alembic from apps/api/ ---
# env.py is at: apps/api/alembic/migrations/env.py
# parents[0]=migrations, [1]=alembic, [2]=api, [3]=apps
SRC_DIR = Path(__file__).resolve().parents[2] / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

# --- Import your app settings & models (models.py pulls in all domain tables) ---
# Prefer central settings via pydantic_settings; fall back to env var if needed.
try:
    from config import get_settings  # type: ignore
    settings = get_settings()
    SQLALCHEMY_URL = settings.DATABASE_URL
except Exception:
    # Fallback to raw env var for local/CI convenience
    SQLALCHEMY_URL = os.getenv("DATABASE_URL")

# Alembic Config object
config = context.config

# Logging (reads loggers from alembic.ini)
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Import models to ensure SQLModel.metadata is populated for autogenerate
try:
    import models  # noqa: F401
except Exception:
    # If you organize by domains (e.g., babies.models), import them here as needed.
    pass

# Target metadata for 'autogenerate'
target_metadata = SQLModel.metadata

# --- Safety checks ---

def _assert_valid_url(url: str | None) -> None:
    if not url:
        raise RuntimeError(
            "[alembic] DATABASE_URL is not set. Provide via config.get_settings() or env var."
        )
    try:
        u = make_url(url)
    except Exception as e:
        raise RuntimeError(f"[alembic] Invalid DATABASE_URL: {e}") from e
    if u.get_backend_name() not in ("postgresql+psycopg", "postgresql"):
        raise RuntimeError(
            f"[alembic] Unexpected driver '{u.get_backend_name()}'. "
            "Expected 'postgresql+psycopg' (psycopg v3) or 'postgresql'."
        )


def _assert_models_loaded() -> None:
    if not SQLModel.metadata.tables:
        raise RuntimeError(
            "[alembic] No tables found in SQLModel.metadata. "
            "Ensure `src/models.py` imports all domain models or import them here."
        )


_assert_valid_url(SQLALCHEMY_URL)
_assert_models_loaded()

# --- Offline migrations ---

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode (outputs SQL rather than executing)."""
    context.configure(
        url=SQLALCHEMY_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
        compare_server_default=True,
    )
    with context.begin_transaction():
        context.run_migrations()


# --- Online migrations ---

def run_migrations_online() -> None:
    """Run migrations in 'online' mode (executes against the DB)."""
    connectable = create_engine(
        SQLALCHEMY_URL,  # type: ignore[arg-type]
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )
        with context.begin_transaction():
            context.run_migrations()


# --- Entrypoint ---
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
