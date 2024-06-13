from datetime import date, datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class FakeBaseOrm(BaseModel):
    pass


class FakeAddTask(FakeBaseOrm):
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


class FakeOrmItem(FakeBaseOrm):
    id: UUID
    product_code: str
    is_aggregated: bool
    aggregated_at: Optional[datetime]
    task_id: UUID

    def aggregated(self) -> None:
        self.is_aggregated = True
        self.aggregated_at = datetime.now()

    def deaggregated(self) -> None:
        self.is_aggregated = False
        self.aggregated_at = None


class FakeOrmCube(FakeOrmItem):
    pass


class FakeOrmProduct(FakeOrmItem):
    pass


class FakeOrmTask(FakeBaseOrm):
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
    products: list[FakeOrmItem]
    cubes: list[FakeOrmItem]

    def update_status_closed(self, status: bool) -> None:
        if status != self.status_closed:
            if status:
                self.closed_at = datetime.now()
            else:
                self.closed_at = None
