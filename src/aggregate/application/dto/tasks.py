from datetime import date, datetime
from typing import Any, Generic, Optional, TypeVar
from uuid import UUID

from pydantic import BaseModel

from aggregate.infra import TaskFilter

from .items import CubeResponse, ProductResponse

DataT = TypeVar("DataT")


class TaskUpdate(BaseModel):
    task_id: UUID
    update_dict: dict[str, Any]


class FilterData(BaseModel):
    page: int
    size: int
    filter: TaskFilter


class Page(BaseModel, Generic[DataT]):
    """DTO модель для получения результатов фильтрации"""

    data: list[DataT]
    page: int
    size: int
    total: int


class AddTask(BaseModel):
    """DTO добавления партии"""

    status_closed: bool
    shift_task_representation: str
    line: str
    shift: str
    brigade: str
    batch_number: int
    batch_date: date
    nomenclature: str
    code_ekn: str
    identifier_rc: str
    shift_start_time: datetime
    shift_end_time: datetime


class TaskResponse(BaseModel):
    """DTO возвращаемой партии"""

    id: UUID
    status_closed: bool
    shift_task_representation: str
    line: str
    shift: str
    brigade: str
    batch_number: int
    batch_date: date
    nomenclature: str
    code_ekn: str
    identifier_rc: str
    shift_start_time: datetime
    shift_end_time: datetime
    closed_at: Optional[datetime]
    products: list[ProductResponse]
    cubes: list[CubeResponse]
