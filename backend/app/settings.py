from functools import lru_cache

from pydantic_settings import BaseSettings

class CoreSettings(BaseSettings):
    APP_NAME: str = "Shop"
    DEBUG: bool = False

class Settings(CoreSettings):
    pass

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()