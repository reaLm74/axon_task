from logging.config import dictConfig

from pydantic import BaseModel


class LogConfig(BaseModel):
    LOGGER_NAME: str = "api"
    LOG_FORMAT: str = "%(levelname)s ::%(module)s|%(lineno)s:: %(message)s"
    LOG_LEVEL: str = "DEBUG"
    version: int = 1
    disable_existing_loggers: bool = False
    formatters: dict = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers: dict = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    }
    loggers: dict = {
        LOGGER_NAME: {"handlers": ["default"], "level": LOG_LEVEL},
    }


def create_logger() -> None:
    dictConfig(LogConfig().model_dump())
