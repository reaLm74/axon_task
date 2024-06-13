import uuid
from datetime import date
from uuid import UUID

from aggregate.domain.entity import Task
from aggregate.infra import TaskFilter
from aggregate.infra.repository.abstract import TasksRepository

from tests.unit.fake.fake_base_orm import FakeOrmTask


class FakeTasksRepository(TasksRepository):
    _data: list[FakeOrmTask] = []

    @property
    def data(self) -> list[FakeOrmTask]:
        return FakeTasksRepository._data

    @data.setter
    def data(self, new_data: list[FakeOrmTask]) -> None:
        FakeTasksRepository._data = new_data

    async def get_by_id(self, task_id: UUID) -> FakeOrmTask | None:
        """Получение партии по id"""
        for item in self.data:
            if item.id == task_id:
                return item
        return None

    async def get_by_num_date(
            self, batch_number: int, batch_date: date
    ) -> FakeOrmTask | None:
        """Получение партии по номеру и дате (уникальная связка)"""
        for item in self.data:
            if item.batch_number == batch_number and item.batch_date == batch_date:
                return item
        return None

    async def get_by_filter(self, product_filter: TaskFilter) -> list[FakeOrmTask]:
        """Получение партий по фильтру"""

        fields = product_filter.model_dump(exclude_none=True, exclude_unset=True)
        result = []
        for item in self.data:
            b = True
            for key in fields:
                if getattr(item, key) != fields[key]:
                    b = False
            if b:
                result.append(item)
        return result

    async def update(self, data: Task) -> None:
        """Обновление партии"""
        pass

    async def create(self, task: Task) -> None:
        """Создание партии"""
        dump_task = task.model_dump()
        dump_task["id"] = uuid.uuid4()
        dump_task["cubes"] = []
        dump_task["products"] = []
        new_task = FakeOrmTask(**dump_task)
        self.data.append(new_task)
