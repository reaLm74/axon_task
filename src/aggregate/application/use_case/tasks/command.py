import math
from typing import Optional

from shared_kernel.infra.uow.base import UnitOfWork

from aggregate.application.dto import (
    AddTask,
    FilterData,
    Page,
    TaskResponse,
    TaskUpdate,
)
from aggregate.domain.entity import Task
from aggregate.domain.exceptions import TaskNotFound


class TaskCommandUseCase:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def add(self, tasks: list[AddTask]) -> None:
        async with self.uow as uow:
            for task in tasks:
                check_tasks: Optional[Task] = await uow.tasks.get_by_num_date(
                    batch_number=task.batch_number,
                    batch_date=task.batch_date,
                )
                if check_tasks is not None:
                    check_tasks.update_status_closed(task.status_closed)
                    patch_dict = task.model_dump(exclude_unset=True)
                    for key, value in patch_dict.items():
                        setattr(check_tasks, key, value)
                    await uow.tasks.update(check_tasks)
                    continue
                create_data = Task(**task.model_dump())
                if create_data.status_closed:
                    create_data.add_closed_at()
                await uow.tasks.create(task=create_data)
            await uow.commit()

    async def filter(self, filter_data: FilterData) -> Page[TaskResponse]:
        offset_min = filter_data.page * filter_data.size
        offset_max = (filter_data.page + 1) * filter_data.size
        async with self.uow as uow:
            list_tasks: list[Task] = await uow.tasks.get_by_filter(filter_data.filter)
        task_response: list[TaskResponse] = [
            TaskResponse.model_validate(task, from_attributes=True)
            for task in list_tasks
        ]
        result = Page[TaskResponse](
            data=task_response[offset_min:offset_max],
            page=filter_data.page,
            size=filter_data.size,
            total=math.ceil(len(list_tasks) / filter_data.size) - 1,
        )
        return result

    async def update(self, update: TaskUpdate) -> TaskResponse:
        async with self.uow as uow:
            task: Task = await uow.tasks.get_by_id(update.task_id)
            if task is None:
                raise TaskNotFound()
            if "status_closed" in update.update_dict:
                task.update_status_closed(update.update_dict["status_closed"])
            for key, value in update.update_dict.items():
                setattr(task, key, value)
            await uow.tasks.update(task)
            await uow.commit()
            task_response = TaskResponse.model_validate(task, from_attributes=True)
            return task_response
