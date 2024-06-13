from datetime import datetime


class OrderException(Exception):
    detail: str
    entity_name: str
    message: str


class NotFoundException(OrderException):
    def __init__(self) -> None:
        self.detail = f"{self.entity_name} not found"


class TaskNotFound(NotFoundException):
    entity_name = "Task"


class ItemNotFound(NotFoundException):
    entity_name = "Item"


class BadRequestException(OrderException):
    def __init__(self) -> None:
        self.detail = self.message


class ErrorProductDeaggregate(BadRequestException):
    message = "Item de-aggregated"


class ErrorCodeUsed(BadRequestException):
    def __init__(self, data: datetime) -> None:
        self.message = f"unique code already used at {data}"
        super().__init__()


class ErrorCodeAttached(BadRequestException):
    message = "unique code is attached to another batch"


class TaskClosed(BadRequestException):
    message = "Task is closed"
