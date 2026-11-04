import os
from pathlib import Path
from typing import List
from dotenv import load_dotenv

# Base directory of the repository
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Load .env if it exists
load_dotenv(BASE_DIR / ".env")


class Settings:
    PROJECT_NAME: str = "PULSE Backend"
    VERSION: str = "0.1.0"
    DESCRIPTION: str = "Proactive Customer Recovery & Assurance Platform API"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "true").lower() in ("true", "1", "t")

    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./pulse.db")
    SQL_ECHO: bool = os.getenv("SQL_ECHO", "false").lower() in ("true", "1", "t")

    HOST: str = os.getenv("HOST", "127.0.0.1")
    PORT: int = int(os.getenv("PORT", "8000"))

    CORS_ORIGINS: List[str] = [
        origin.strip()
        for origin in os.getenv(
            "CORS_ORIGINS",
            "http://localhost:3000,http://localhost:5173,http://127.0.0.1:3000,http://127.0.0.1:5173",
        ).split(",")
        if origin.strip()
    ]


settings = Settings()

