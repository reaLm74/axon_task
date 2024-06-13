from datetime import date, datetime
from typing import Optional, TypeVar
from uuid import UUID

from pydantic import BaseModel, Field

DataT = TypeVar("DataT")


class TaskIn(BaseModel):
    """DTO создание модели партии"""

    status_closed: bool = Field(..., validation_alias="СтатусЗакрытия")
    shift_task_representation: str = Field(
        ..., validation_alias="ПредставлениеЗаданияНаСмену"
    )
    line: str = Field(..., validation_alias="Линия")
    shift: str = Field(..., validation_alias="Смена")
    brigade: str = Field(..., validation_alias="Бригада")
    batch_number: int = Field(..., validation_alias="НомерПартии")
    batch_date: date = Field(..., validation_alias="ДатаПартии")
    nomenclature: str = Field(..., validation_alias="Номенклатура")
    code_ekn: str = Field(..., validation_alias="КодЕКН")
    identifier_rc: str = Field(..., validation_alias="ИдентификаторРЦ")
    shift_start_time: datetime = Field(..., validation_alias="ДатаВремяНачалаСмены")
    shift_end_time: datetime = Field(..., validation_alias="ДатаВремяОкончанияСмены")


class ItemIn(BaseModel):
    """DTO куба"""

    product_code: str = Field(..., validation_alias="УникальныйКод")
    batch_number: int = Field(..., validation_alias="НомерПартии")
    batch_date: date = Field(..., validation_alias="ДатаПартии")


class AggregationId(BaseModel):
    """DTO аггрегации по ID"""

    task_id: UUID
    product_code: str


class AggregationDataNumber(BaseModel):
    """DTO аггрегации по дате и номеру партии"""

    batch_date: date
    batch_number: int
    product_code: str


class SearchId(AggregationId):
    """DTO поиска по ID"""


class SearchDataNumber(AggregationDataNumber):
    """DTO поиска по дате и номеру партии"""


class TaskPatch(BaseModel):
    """DTO update партии"""

    status_closed: Optional[bool] = None
    shift_task_representation: Optional[str] = None
    line: Optional[str] = None
    shift: Optional[str] = None
    brigade: Optional[str] = None
    batch_number: Optional[int] = None
    batch_date: Optional[date] = None
    nomenclature: Optional[str] = None
    code_ekn: Optional[str] = None
    identifier_rc: Optional[str] = None
    shift_start_time: Optional[datetime] = None
    shift_end_time: Optional[datetime] = None
