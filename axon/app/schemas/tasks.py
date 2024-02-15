from datetime import date, datetime
from typing import List, Optional

from app.schemas.products import ReadProduct
from pydantic import BaseModel, Field


class ShiftTask(BaseModel):
    status_closed: Optional[bool] = Field(
        None, validation_alias='СтатусЗакрытия'
    )
    shift_task_representation: Optional[str] = Field(
        None, validation_alias='ПредставлениеЗаданияНаСмену'
    )
    line: Optional[str] = Field(None, validation_alias='Линия')
    shift: Optional[str] = Field(None, validation_alias='Смена')
    brigade: Optional[str] = Field(None, validation_alias='Бригада')
    batch_number: Optional[int] = Field(None, validation_alias='НомерПартии')
    batch_date: Optional[date] = Field(None, validation_alias='ДатаПартии')
    nomenclature: Optional[str] = Field(None, validation_alias='Номенклатура')
    code_ekn: Optional[str] = Field(None, validation_alias='КодЕКН')
    identifier_rc: Optional[str] = Field(
        None, validation_alias='ИдентификаторРЦ'
    )
    shift_start_time: Optional[datetime] = Field(
        None, validation_alias='ДатаВремяНачалаСмены'
    )
    shift_end_time: Optional[datetime] = Field(
        None, validation_alias='ДатаВремяОкончанияСмены'
    )


class ReadTask(BaseModel):
    id: int
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
    products: List[ReadProduct]


class FilterTask(BaseModel):
    data: List[ReadTask]
    page: int
    size: int
    total: int
