from dotenv import load_dotenv
from sqlalchemy import URL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

load_dotenv()


class Settings:

    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_SERVER: str = os.getenv(
        "POSTGRES_SERVER",
        "localhost",
    )
    POSTGRES_PORT: str = os.getenv(
        "POSTGRES_PORT",
        5432,
    )
    POSTGRES_DB: str = os.getenv(
        "POSTGRES_DB",
        "tdd",
    )
    DATABASE_URL = URL.create(
        "postgresql",
        POSTGRES_USER,
        POSTGRES_PASSWORD,
        POSTGRES_SERVER,
        int(POSTGRES_PORT),
        POSTGRES_DB,
    )


settings = Settings()

# Create the SQLAlchemy engine
engine = create_engine(settings.DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency for getting the database session
def get_db():
    """
    Dependency to get a SQLAlchemy database session.
    This function is used in FastAPI endpoints to ensure that
    each request gets a fresh database session, and that session
    is properly closed after the request is handled.

    Yields:
        db (Session): SQLAlchemy session for database operations.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
