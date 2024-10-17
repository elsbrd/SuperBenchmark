import os

from pydantic_settings import BaseSettings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Settings(BaseSettings):
    BASE_DIR: str = BASE_DIR
    SUPERBENCHMARK_DEBUG: bool = False

    class Config:
        env_file = os.path.join(BASE_DIR, ".env")


settings = Settings()
