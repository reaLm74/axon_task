from datetime import date
from uuid import UUID

from shared_kernel.infra.uow.base import UnitOfWork

from aggregate.application.dto import TaskResponse
from aggregate.domain.entity import Task
from aggregate.domain.exceptions import TaskNotFound


class TaskQueryUseCase:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def get_by_id(self, task_id: UUID) -> TaskResponse:
        async with self.uow as uow:
            task: Task = await uow.tasks.get_by_id(task_id=task_id)
            if task is None:
                raise TaskNotFound()
            task_response = TaskResponse.model_validate(task, from_attributes=True)
            return task_response

    async def get_by_num_date(
        self, batch_number: str, batch_date: date
    ) -> TaskResponse:
        async with self.uow as uow:
            task: Task = await uow.tasks.get_by_num_date(batch_number, batch_date)
            if task is None:
                raise TaskNotFound()
            task_response = TaskResponse.model_validate(task, from_attributes=True)
            return task_response
