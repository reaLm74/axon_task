from typing import List

from fastapi import APIRouter, HTTPException
from fastapi import status
from fastapi_filter import FilterDepends
from sqlalchemy.exc import SQLAlchemyError

from app.filter.tasks import TaskFilter
from app.schemas.tasks import ShiftTask, ReadTask
from app.services.tasks import TaskRepository
from app.utils.exception import TaskNotFound

router = APIRouter(
    prefix="/tasks",
    tags=["Task"],
)


@router.get(
    "/{task_id}", status_code=status.HTTP_200_OK, response_model=ReadTask
)
async def get_task(task_id: int):
    try:
        return await TaskRepository().get_task(task_id)
    except TaskNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    except SQLAlchemyError as error:
        raise SQLAlchemyError(f'Error in "get_task": {error}')


@router.get("", status_code=status.HTTP_200_OK, response_model=List[ReadTask])
async def filter_task(product_filter: TaskFilter = FilterDepends(TaskFilter)):
    try:
        return await TaskRepository().filter_task(product_filter)
    except SQLAlchemyError as error:
        raise SQLAlchemyError(f'Error in "filter_task": {error}')


@router.post("/add", status_code=status.HTTP_201_CREATED)
async def add_task(new_tasks: List[ShiftTask]):
    try:
        await TaskRepository().add_task(new_tasks)
    except SQLAlchemyError as error:
        raise SQLAlchemyError(f'Error in "add_task": {error}')


@router.patch(
    "/{task_id}", status_code=status.HTTP_201_CREATED, response_model=ReadTask
)
async def update_task(task_id: int, update: ShiftTask):
    try:
        return await TaskRepository().update_task(task_id, update)
    except TaskNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    except SQLAlchemyError as error:
        raise SQLAlchemyError(f'Error in "update_task": {error}')
