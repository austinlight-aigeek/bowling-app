import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.base import Base, get_db

# Use SQLite in-memory database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Override the database dependency to use the test database
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="module")
def setup_database():
    """
    Setup test database before running tests, and teardown after.
    """
    # Create the test database schema
    Base.metadata.create_all(bind=engine)
    yield
    # Drop the test database schema after the tests
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="module")
def client():
    """
    Create a TestClient instance for FastAPI.
    """
    return TestClient(app)
