from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional


class Product(BaseModel):
    product_code: str = Field(..., validation_alias='УникальныйКодПродукта')
    batch_number: int = Field(..., validation_alias='НомерПартии')
    batch_date: date = Field(..., validation_alias='ДатаПартии')


class ReadProduct(BaseModel):
    id: int
    product_code: str
    is_aggregated: bool
    aggregated_at: Optional[datetime]
    task_id: int
