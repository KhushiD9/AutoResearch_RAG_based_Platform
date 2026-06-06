from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    GEMINI_API_KEY: str = ""
    DATABASE_URL: Optional[str] = None
    SECRET_KEY: str = "change-in-production"

    class Config:
        env_file = ".env"

settings = Settings()
