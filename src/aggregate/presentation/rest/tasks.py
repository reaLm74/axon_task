import logging
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query, status
from fastapi_filter import FilterDepends
from shared_kernel.infra.container import AppContainer
from sqlalchemy.exc import SQLAlchemyError

from aggregate.application.dto import (
    AddTask,
    FilterData,
    Page,
    TaskResponse,
    TaskUpdate,
)
from aggregate.application.use_case.tasks import (
    TaskCommandUseCase,
    TaskQueryUseCase,
)
from aggregate.domain.exceptions import TaskNotFound
from aggregate.infra import TaskFilter
from aggregate.presentation.dto import TaskDetail, TaskIn, TaskPatch
from aggregate.presentation.exceptions import Message, NotFound, SQLError

logger = logging.getLogger("api")
router = APIRouter(
    prefix="/tasks",
    tags=["Task"],
)


@router.get(
    path="",
    status_code=status.HTTP_200_OK,
    response_model=Page[TaskDetail],
    responses={status.HTTP_400_BAD_REQUEST: {"model": Message}},
)
@inject
async def filter_task(
    filter_parameters: TaskFilter = FilterDepends(TaskFilter),
    page: int = Query(ge=0, default=0),
    size: int = Query(ge=1, le=100, default=10),
    task_command: TaskCommandUseCase = Depends(Provide[AppContainer.task_command]),
) -> Page[TaskDetail]:
    try:
        logger.info("Запрос на фильтрацию партий")
        filter_data = FilterData(page=page, size=size, filter=filter_parameters)
        result: Page[TaskResponse] = await task_command.filter(filter_data)
        data: list[TaskDetail] = [
            TaskDetail.model_validate(task, from_attributes=True)
            for task in result.data
        ]
        page = result.page
        size = result.size
        total = result.total
        return Page[TaskDetail](data=data, page=page, size=size, total=total)
    except SQLAlchemyError:
        raise SQLError()


@router.get(
    path="/{task_id}",
    status_code=status.HTTP_200_OK,
    response_model=TaskDetail,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": Message},
        status.HTTP_400_BAD_REQUEST: {"model": Message},
    },
)
@inject
async def get_task_by_id(
    task_id: UUID,
    task_query: TaskQueryUseCase = Depends(Provide[AppContainer.task_query]),
) -> TaskDetail:
    try:
        logger.info("Запрос партии по id")
        result: TaskResponse = await task_query.get_by_id(task_id)
        return TaskDetail.model_validate(result, from_attributes=True)
    except TaskNotFound as e:
        raise NotFound(detail=e.detail)
    except SQLAlchemyError:
        raise SQLError()


@router.post(
    path="/add",
    status_code=status.HTTP_201_CREATED,
    responses={status.HTTP_400_BAD_REQUEST: {"model": Message}},
)
@inject
async def add_task(
    new_tasks: list[TaskIn],
    task_command: TaskCommandUseCase = Depends(Provide[AppContainer.task_command]),
) -> None:
    try:
        logger.info("Создание партии")
        tasks: list[AddTask] = [
            AddTask.model_validate(task, from_attributes=True) for task in new_tasks
        ]
        await task_command.add(tasks)
    except SQLAlchemyError:
        raise SQLError()


@router.patch(
    path="/{task_id}",
    status_code=status.HTTP_201_CREATED,
    response_model=TaskDetail,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": Message},
        status.HTTP_400_BAD_REQUEST: {"model": Message},
    },
)
@inject
async def update_task(
    task_id: UUID,
    update: TaskPatch,
    task_command: TaskCommandUseCase = Depends(Provide[AppContainer.task_command]),
) -> TaskDetail:
    try:
        logger.info(f"Обновление партии {task_id}")
        patch_dict = update.model_dump(exclude_unset=True)
        update_data = TaskUpdate(task_id=task_id, update_dict=patch_dict)
        result: TaskResponse = await task_command.update(update_data)
        return TaskDetail.model_validate(result, from_attributes=True)
    except TaskNotFound as e:
        raise NotFound(detail=e.detail)
    except SQLAlchemyError:
        raise SQLError()
