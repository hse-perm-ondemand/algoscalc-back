from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.internal.constants import DEFAULT_ALGORITHMS_CATALOG_PATH


class Settings(BaseSettings):
    """Класс конфигурируемые параметры приложения. Параметры могут быть переопределены
    в файле .env в корне проекта или через переменные окружения."""

    EXECUTE_TIMEOUT: int = 0
    ALGORITHMS_CATALOG_PATH: str = DEFAULT_ALGORITHMS_CATALOG_PATH
    BACKEND_CORS_ORIGINS: list[str | AnyHttpUrl] = [
        "https://test.ommat.ru",
        "https://prod.ommat.ru",
    ]
    USE_LOGGER: bool = True
    LOG_LEVEL: str = "WARNING"
    VERSION: str = "local-build"

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=True
    )


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s %(funcName)s: %(message)s"
        }
    },
    "handlers": {
        "default": {
            "level": "DEBUG",
            "formatter": "standard",
            "class": "logging.StreamHandler",
        },
        "file_handler": {
            "level": "DEBUG",
            "formatter": "standard",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "./logs/app.log",
            "encoding": "utf8",
            "maxBytes": 10240000,
            "backupCount": 5,
        },
    },
    "loggers": {
        "": {
            "handlers": ["file_handler", "default"],
            "level": "WARNING",
            "propagate": True,
        }
    },
}
