import logging

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=True, env_prefix="BINGO_")

    LOG_LEVEL: int = logging.DEBUG

    LOGGING_FORMAT: str = "[%(asctime)s][%(name)s][%(levelname)s] %(message)s"

    HOST: str = "127.0.0.1"
    PORT: int = 8000

    BOARD_SIZE: int = 5


settings = Settings()
