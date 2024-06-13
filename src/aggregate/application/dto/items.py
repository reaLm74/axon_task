from datetime import date, datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class AddItem(BaseModel):
    """DTO добавления продукции"""

    batch_date: date
    batch_number: int
    product_code: str


class AggregateIdItem(BaseModel):
    """DTO аггрегации/деаггрегации продукции по ID партии"""

    task_id: UUID
    product_code: str


class AggregateDataNumberItem(BaseModel):
    """DTO аггрегации/деаггрегации продукции по дате и номеру партии"""

    batch_date: date
    batch_number: int
    product_code: str


class SearchIdItem(AggregateIdItem):
    """DTO поиска по ID"""


class SearchDataNumberItem(AggregateDataNumberItem):
    """DTO поиска по дате и номеру партии"""


class FieldSearchItem(BaseModel):
    """DTO добавления продукции"""

    task_id: UUID
    product_code: str


class ItemResponse(BaseModel):
    """DTO возвращаемой продукции"""

    id: UUID
    product_code: str
    is_aggregated: bool
    aggregated_at: Optional[datetime]
    task_id: UUID


class CubeResponse(ItemResponse):
    """DTO возвращаемого куба"""


class ProductResponse(ItemResponse):
    """DTO возвращаемого продукта"""
