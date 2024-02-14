from typing import List

from fastapi import APIRouter
from fastapi import status
from fastapi_filter import FilterDepends

from app.filter.tasks import TaskFilter
from app.schemas.tasks import ShiftTask, ReadTask
from app.services import tasks

router = APIRouter(
    prefix="/tasks",
    tags=["Task"],
)


@router.get(
    "/{task_id}", status_code=status.HTTP_200_OK, response_model=ReadTask
)
async def get_task(task_id: int):
    return await tasks.get_task(task_id)


@router.get("", status_code=status.HTTP_200_OK, response_model=List[ReadTask])
async def filter_task(product_filter: TaskFilter = FilterDepends(TaskFilter)):
    return await tasks.filter_task(product_filter)


@router.post("/add", status_code=status.HTTP_201_CREATED)
async def add_task(new_tasks: List[ShiftTask]):
    await tasks.add_task(new_tasks)


@router.patch(
    "/{task_id}", status_code=status.HTTP_201_CREATED, response_model=ReadTask
)
async def update_task(task_id: int, update: ShiftTask):
    return await tasks.update_task(task_id, update)
