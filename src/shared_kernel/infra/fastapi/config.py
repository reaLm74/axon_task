import os

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class Settings(BaseSettings):
    DRIVER: str = Field(default="postgresql+asyncpg")
    DB_HOST: str = Field(default="localhost")
    DB_PASS: str = Field(default="postgres")
    DB_NAME: str = Field(default="postgres")
    DB_USER: str = Field(default="postgres")
    DB_PORT: str = Field(default="5432")

    model_config = SettingsConfigDict(env_file=".env")

    TIMEDELTA_MINUTES_MIN: int = Field(default=40)
    TIMEDELTA_MINUTES_MAX: int = Field(default=75)

    OTEL: bool = Field(default=True)


settings = Settings()


DATABASE_URL = (
    f"{settings.DRIVER}://{settings.DB_USER}:{settings.DB_PASS}@"
    f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
)
