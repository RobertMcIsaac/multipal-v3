from pathlib import Path
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str

    model_config = SettingsConfigDict(
        # env_file=Path(__file__).resolve().parents[1] / ".env",
            # if starting from repo root, use above
        env_file="./.env",
        env_ignore_empty=True,
        extra="ignore",
    )

@lru_cache
def get_settings() -> Settings:
    return Settings()