from datetime import date, datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class AggregationOut(BaseModel):
    """DTO вывода по результату аггрегации"""

    product_code: str


class ItemDetail(BaseModel):
    """DTO вывода продукции"""

    id: UUID
    product_code: str
    is_aggregated: bool
    aggregated_at: Optional[datetime]
    task_id: UUID


class CubeDetail(ItemDetail):
    """DTO вывода куба"""


class ProductDetail(ItemDetail):
    """DTO вывода продукта"""


class TaskDetail(BaseModel):
    """DTO вывода партии"""

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
    products: list[ProductDetail]
    cubes: list[CubeDetail]
