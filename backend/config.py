from pydantic import BaseSettings, Field, ValidationError
from typing import List, Optional
import os

class Settings(BaseSettings):
    OPENAI_API_KEY: str = Field(..., env="OPENAI_API_KEY")
    AZURE_OPENAI_ENDPOINT: Optional[str] = Field(None, env="AZURE_OPENAI_ENDPOINT")
    VECTOR_DB_PATH: str = Field("/app/shared-data/providers.json", env="VECTOR_DB_PATH")
    FRONTEND_URL: str = Field(..., env="FRONTEND_URL")
    CORS_ORIGINS: str = Field("*", env="CORS_ORIGINS")
    LOG_LEVEL: str = Field("info", env="LOG_LEVEL")
    ENV: str = Field("production", env="ENV")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = None
try:
    settings = Settings()
    print(f"[BOOT] ENV: {settings.ENV}, LogLevel: {settings.LOG_LEVEL}, VectorDB: {settings.VECTOR_DB_PATH}")
    if settings.ENV != "production":
        print("[WARNING] Running in development mode on production infra!")
except ValidationError as e:
    print("[ERROR] Missing required environment variables:", e)
    raise 