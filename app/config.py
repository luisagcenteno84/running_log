from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    app_name: str = 'Running Tracker API'
    environment: str = Field(default='development', alias='ENVIRONMENT')
    secret_key: str = Field(default='change-me', alias='SECRET_KEY')
    api_v1_prefix: str = '/api/v1'
    google_cloud_project: str | None = Field(default=None, alias='GOOGLE_CLOUD_PROJECT')


@lru_cache
def get_settings() -> Settings:
    return Settings()
