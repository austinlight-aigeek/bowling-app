import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.base import Base, get_db
from fastapi.testclient import TestClient
from app.main import app

# SQLite in-memory database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

# Create an engine for SQLite in-memory database
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Create a configured session factory for SQLite in-memory database
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Override the `get_db` dependency to use the testing database session
@pytest.fixture(scope="module")
def db():
    # Create the tables in the database
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.close()
        # Drop the tables after the tests
        Base.metadata.drop_all(bind=engine)


# FastAPI client for integration testing
@pytest.fixture(scope="module")
def client():
    # Override the database dependency with the testing session
    app.dependency_overrides[get_db] = db
    with TestClient(app) as test_client:
        yield test_client
