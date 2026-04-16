"""Application configuration from environment variables."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://scires:scires_secret@db:5432/scires_db"
    SECRET_KEY: str = "dev-secret-key-change-in-production-abc123xyz"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60  # 1 hour
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 43200  # 30 days

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
