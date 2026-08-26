from functools import lru_cache
import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    groq_api_key: str | None = None
    groq_model: str = "openai/gpt-oss-20b"
    groq_timeout_seconds: float = 30.0
    app_name: str = "Performance Scoring Engine"
    app_version: str = "2.0.0"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
