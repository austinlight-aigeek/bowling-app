from dotenv import load_dotenv
from sqlalchemy import URL
import os

load_dotenv()


class Settings:

    # Check if DATABASE_URL is already set in the environment
    DATABASE_URL: str = os.getenv("DATABASE_URL")

    if not DATABASE_URL:
        # If DATABASE_URL is not provided, construct it from individual components
        POSTGRES_USER: str = os.getenv("POSTGRES_USER")
        POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
        POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
        POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
        POSTGRES_DB: str = os.getenv("POSTGRES_DB", "tdd")

        # Dynamically create the DATABASE_URL using SQLAlchemy's URL.create
        DATABASE_URL = URL.create(
            "postgresql",
            POSTGRES_USER,
            POSTGRES_PASSWORD,
            POSTGRES_SERVER,
            int(POSTGRES_PORT),
            POSTGRES_DB,
        )


settings = Settings()
