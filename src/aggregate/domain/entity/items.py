from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from shared_kernel.infra.fastapi.meter import record_aggregated, record_deaggregated


class Item(BaseModel):
    id: Optional[UUID] = None
    product_code: str
    is_aggregated: Optional[bool] = None
    aggregated_at: Optional[datetime] = None
    task_id: UUID

    def aggregated(self, name) -> None:
        self.is_aggregated = True
        self.aggregated_at = datetime.now()
        record_aggregated(name)

    def deaggregated(self, name) -> None:
        self.is_aggregated = False
        self.aggregated_at = None
        record_deaggregated(name)
