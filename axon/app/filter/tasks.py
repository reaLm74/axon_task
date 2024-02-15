from datetime import date
from typing import List, Optional

from app.models.tasks import TaskTable
from fastapi_filter.contrib.sqlalchemy import Filter


class TaskFilter(Filter):
    status_closed: Optional[bool] = None
    shift_task_representation: Optional[str] = None
    line: Optional[str] = None
    shift: Optional[str] = None
    brigade: Optional[str] = None
    batch_number: Optional[int] = None
    batch_date: Optional[date] = None
    nomenclature: Optional[str] = None

    order_by: List[str] = ["batch_number"]

    class Constants(Filter.Constants):
        model = TaskTable
