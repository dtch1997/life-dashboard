"""Database connection and session management."""

import os
from contextlib import contextmanager
from pathlib import Path
from typing import Generator

from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session

from storage.models import Base


def get_engine() -> Engine:
    """Get SQLAlchemy engine based on environment configuration.

    Returns:
        Engine configured for either SQLite (local dev) or PostgreSQL (production)

    Environment variables:
        DB_TYPE: "sqlite" (default) or "postgres"
        DATABASE_URL: PostgreSQL connection string (required if DB_TYPE=postgres)
    """
    db_type = os.getenv("DB_TYPE", "sqlite")

    if db_type == "sqlite":
        # Create database directory if it doesn't exist
        db_path = Path.home() / ".life-dashboard" / "data.db"
        db_path.parent.mkdir(parents=True, exist_ok=True)
        return create_engine(f"sqlite:///{db_path}")
    elif db_type == "postgres":
        db_url = os.getenv("DATABASE_URL")
        if not db_url:
            raise ValueError("DATABASE_URL environment variable required for postgres")
        return create_engine(db_url)
    else:
        raise ValueError(f"Unsupported DB_TYPE: {db_type}. Use 'sqlite' or 'postgres'")


def init_db(engine: Engine) -> None:
    """Initialize database by creating all tables.

    Args:
        engine: SQLAlchemy engine to use for table creation
    """
    Base.metadata.create_all(engine)


@contextmanager
def get_session() -> Generator[Session, None, None]:
    """Context manager for database sessions.

    Handles transaction management:
    - Commits on successful completion
    - Rolls back on exceptions
    - Always closes the session

    Yields:
        Database session

    Example:
        with get_session() as session:
            obj = StoredObject(...)
            session.add(obj)
        # Automatically committed and closed
    """
    engine = get_engine()
    init_db(engine)  # Ensure tables exist
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
