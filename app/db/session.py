from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
from core.config import settings

# Create SQLAlchemy engine
# For SQLite, we need check_same_thread=False to allow multi-threaded access
# For other databases, this argument is ignored
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {},
    echo=False,  # Set to True for SQL query logging during development
    pool_pre_ping=True  # Verify connections before using them
)

# Create session factory
sessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db() -> Generator[Session, None, None]:
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()