import logging
from typing import Any

from fastapi import HTTPException, status
from pydantic import BaseModel

logger = logging.getLogger("api")


class BadRequest(HTTPException):
    def __init__(self, detail: Any = "Bad request") -> None:
        logger.error("%s", detail)
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class NotFound(HTTPException):
    def __init__(self, detail: Any = "Not found") -> None:
        logger.error("%s", detail)
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class SQLError(HTTPException):
    def __init__(self, detail: Any = "Bad request SQL error") -> None:
        logger.error("%s", detail)
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class Message(BaseModel):
    """DTO вывода исключений"""

    detail: str
