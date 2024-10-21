import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.main import app
from app.db.base import Base, get_db
from app.db.models import Game, Frame

# Path to the test database
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"

# Create an engine and session for the test database
engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create a session factory
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    """
    Create a new database session for a test.

    This fixture will create a new session for every test and roll back any changes after the test is done.
    """
    # Ensure all tables are created before starting the test
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        # Rollback any changes and close the session after each test
        db.rollback()
        db.close()
        # Drop all tables after the test to start fresh for each test
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    """
    Create a new FastAPI test client with the test database.

    This fixture overrides the FastAPI dependency on the real database with the test database.
    """

    # Override the FastAPI dependency for `get_db` to use the test session
    def override_get_db():
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    # Create a TestClient for sending HTTP requests in tests
    with TestClient(app) as test_client:
        yield test_client
