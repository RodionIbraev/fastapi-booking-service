from functools import lru_cache

from pydantic import Field, PostgresDsn, RedisDsn, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "booking-service"
    debug: bool = False
    cors_allow_origins: str = ""
    api_prefix: str = "/api/v1"

    database_url: PostgresDsn = PostgresDsn(
        "postgresql+asyncpg://booking:booking@localhost:5432/booking"
    )
    db_pool_size: int = 10
    db_max_overflow: int = 10

    redis_url: RedisDsn = RedisDsn("redis://localhost:6379/0")
    redis_socket_timeout: float = 0.5

    jwt_secret: SecretStr = Field(min_length=32)
    jwt_algorithm: str = "HS256"
    access_token_ttl_seconds: int = 15 * 60
    refresh_token_ttl_seconds: int = 30 * 24 * 60 * 60

    booking_ttl_seconds: int = 10 * 60
    availability_cache_ttl_seconds: int = 10

    expiry_worker_interval_seconds: float = 5.0
    expiry_worker_batch_size: int = 500


@lru_cache
def get_settings() -> Settings:
    return Settings()
