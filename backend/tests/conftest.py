import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.models import Base
from app.db.base import engine, SessionLocal

"""
This module contains the fixture configurations for testing the FastAPI bowling game API.
It sets up a test client, the test database, and database sessions for unit and integration tests.
"""


# Fixture to create a TestClient for testing the FastAPI app
@pytest.fixture(scope="module")
def client():
    """
    Creates a new FastAPI test client to interact with the API during tests.

    Yields:
        TestClient: An instance of FastAPI's TestClient for making API calls.
    """
    with TestClient(app) as c:
        yield c


# Fixture to set up and tear down the test database
@pytest.fixture(scope="module")
def setup_db():
    """
    Sets up the database for the entire test module and ensures the tables are created.
    Tears down the database (drops all tables) after the test module completes.
    """
    # Create all tables before tests
    Base.metadata.create_all(bind=engine)
    # Provide setup functionality
    yield
    # Drop all tables after tests
    Base.metadata.drop_all(bind=engine)


# Fixture to provide a new session for each test function
@pytest.fixture(scope="function")
def db_session():
    """
    Provides a new database session for each individual test.

    Yields:
        Session: A SQLAlchemy session object for interacting with the database during tests.
    """
    session = SessionLocal()
    try:
        yield session
    finally:
        # Close the session after each test
        session.close()
