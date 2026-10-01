from functools import lru_cache
from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL


SERVER_DIR = Path(__file__).resolve().parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=SERVER_DIR / ".env",
        env_prefix="LIFE_DB_",
        extra="ignore",
    )

    host: str
    port: int = 5432
    name: str
    user: str
    password: SecretStr
    sql_echo: bool = False

    @property
    def database_url(self) -> URL:
        return URL.create(
            drivername="postgresql+asyncpg",
            username=self.user,
            password=self.password.get_secret_value(),
            host=self.host,
            port=self.port,
            database=self.name,
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()
