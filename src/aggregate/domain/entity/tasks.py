from datetime import date, datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from .items import Item
from shared_kernel.infra.fastapi.meter import close_task


class Task(BaseModel):
    id: Optional[UUID] = None
    status_closed: Optional[bool] = None
    shift_task_representation: Optional[str] = None
    line: Optional[str] = None
    shift: Optional[str] = None
    brigade: Optional[str] = None
    batch_number: int
    batch_date: date
    nomenclature: Optional[str] = None
    code_ekn: Optional[str] = None
    identifier_rc: Optional[str] = None
    shift_start_time: Optional[datetime] = None
    shift_end_time: Optional[datetime] = None
    closed_at: Optional[datetime] = None
    products: Optional[list[Item]] = None
    cubes: Optional[list[Item]] = None

    def update_status_closed(self, status: bool) -> None:
        if status != self.status_closed:
            if status:
                self.closed_at = datetime.now()
                close_task.add(1)
            else:
                self.closed_at = None
                close_task.add(-1)

    def add_closed_at(self) -> None:
        self.closed_at = datetime.now()
