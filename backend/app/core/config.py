from dotenv import load_dotenv
from sqlalchemy import URL
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
