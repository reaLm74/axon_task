from datetime import date
from typing import Union
from uuid import UUID

from opentelemetry import trace
from shared_kernel.infra.db.data_mappers import task_to_model
from shared_kernel.infra.db.orm import TaskTable
from shared_kernel.infra.fastapi.meter import record_total
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from aggregate.domain.entity import Task
from aggregate.infra import TaskFilter
from aggregate.infra.repository import SQLABaseRepository
from aggregate.infra.repository.abstract import TasksRepository

tracer = trace.get_tracer(__name__)


class SQLATasksRepository(SQLABaseRepository, TasksRepository):
    """Репозиторий для партий"""

    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=TaskTable)

    async def get_by_id(self, task_id: UUID) -> Union[Task, None]:
        """Получение партии по id"""

        with tracer.start_as_current_span(f"sqlalchemy.{self.name}.get_by_id"):
            query = (
                select(self.model)
                .filter(self.model.id == task_id)
                .options(
                    selectinload(self.model.products),
                    selectinload(self.model.cubes),
                )
            )
            result = await self.session.scalar(query)
            if result is None:
                return None
            self._identity_map["task"] = result
            entity: Task = await task_to_model(result)
            return entity

    async def get_by_num_date(
        self, batch_number: int, batch_date: date
    ) -> Union[Task, None]:
        """Получение партии по номеру и дате (уникальная связка)"""

        with tracer.start_as_current_span(f"sqlalchemy.{self.name}.get_by_num_date"):
            query = (
                select(self.model)
                .filter(
                    and_(
                        self.model.batch_number == batch_number,
                        self.model.batch_date == batch_date,
                    )
                )
                .options(
                    selectinload(self.model.products),
                    selectinload(self.model.cubes),
                )
            )
            result = await self.session.scalar(query)
            if result is None:
                return None
            self._identity_map["task"] = result
            entity: Task = await task_to_model(result)
            return entity

    async def get_by_filter(
        self, product_filter: TaskFilter
    ) -> Union[list[Task], None]:
        """Получение партий по фильтру"""

        with tracer.start_as_current_span(f"sqlalchemy.{self.name}.get_by_filter"):
            query = product_filter.filter(
                select(self.model).options(
                    selectinload(self.model.products),
                    selectinload(self.model.cubes),
                )
            )
            query_sort = product_filter.sort(query)
            result = await self.session.execute(query_sort)
            filtered_data = result.scalars().all()
            list_tasks: list[Task] = [
                await task_to_model(task) for task in filtered_data
            ]
            return list_tasks

    async def update(self, data: Task) -> None:
        """Обновление партии"""

        old_task = self._identity_map["task"]
        patch_dict = data.model_dump(exclude={"id", "products", "cubes"})
        for key, value in patch_dict.items():
            setattr(old_task, key, value)
        self.session.add(old_task)

    async def create(self, task: Task) -> None:
        """Создание партии"""

        new_task = self.model(**task.model_dump(exclude={"products", "cubes"}))
        self.session.add(new_task)
        record_total(self.name)
