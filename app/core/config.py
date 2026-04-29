# app/core/config.py — Application Configuration

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str = "change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 30  # 30 days

    DATABASE_URL: str = "sqlite:///./gramseva.db"

    class Config:
        env_file = ".env"

settings = Settings()