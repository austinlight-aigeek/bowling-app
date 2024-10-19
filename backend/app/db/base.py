from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import settings

DATABASE_URL = settings.DATABASE_URL

# SQLAlchemy engine for PostgreSQL
engine = create_engine(DATABASE_URL)

# Session local class for managing database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for SQLAlchemy models
Base = declarative_base()


# Dependency for getting DB session
def get_db():
    """
    Dependency that provides a database session for each request.

    Yields:
        db: Database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
