"""
Configuration management for Elite Wall Pro API
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # ==========================
    # API Settings
    # ==========================
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_debug: bool = False
    api_secret_key: str = "change-me-in-production"

    # ==========================
    # Supabase
    # ==========================
    supabase_url: str
    supabase_anon_key: str
    supabase_service_key: Optional[str] = None

    # ==========================
    # CORS
    # ==========================
    cors_origins: List[str]

    # ==========================
    # AI / ML
    # ==========================
    anthropic_api_key: Optional[str] = None

    # ==========================
    # Rate Limiting
    # ==========================
    rate_limit_per_minute: int = 60
    rate_limit_per_hour: int = 1000

    # ==========================
    # JWT
    # ==========================
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    refresh_token_expire_days: int = 7

    # ==========================
    # Pydantic v2 config
    # ==========================
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
