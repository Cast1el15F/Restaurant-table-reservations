"""Конфигурация приложения"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Настройки приложения"""

    DATABASE_URL: str = "sqlite:///./restaurant.db"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings: Settings = Settings()
DATABASE_URL: str = settings.DATABASE_URL
