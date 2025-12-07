from functools import lru_cache

from pydantic_settings import BaseSettings


class CoreSettings(BaseSettings):
    APP_NAME: str = "Shop"
    DEBUG: bool = False


class PostgresSettings(BaseSettings):
    PGHOST: str
    PGDATABASE: str
    PGUSER: str
    PGPASSWORD: str
    PGPORT: int = 5432

    @property
    def DATABASE_ASYNC_URL(self) -> str:
        return f"postgresql+asyncpg://{self.PGUSER}:{self.PGPASSWORD}@{self.PGHOST}:{self.PGPORT}/{self.PGDATABASE}"


class JWTSettings(BaseSettings):
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_TIME_MINUTES: int = 5
    REFRESH_TOKEN_TIME_MINUTES: int = 60


class RedisSettings(BaseSettings):
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_USERNAME: str
    REDIS_PASSWORD: str
    REDIS_DATABASE: int = 0


class Settings(CoreSettings, PostgresSettings, JWTSettings, RedisSettings):
    SENTRY_DNS: str
    BETTER_STACK_TOKEN: str
    BETTER_STACK_URL: str


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
