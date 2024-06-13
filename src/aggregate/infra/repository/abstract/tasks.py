from datetime import date
from typing import Any, List, Union
from uuid import UUID

from aggregate.infra import TaskFilter

from .base import BaseRepository


class TasksRepository(BaseRepository):
    """Репозиторий для партий"""

    async def get_by_id(self, task_id: UUID) -> Union[Any, None]:
        """Получение партии по id"""
        pass

    async def get_by_num_date(
        self, batch_number: int, batch_date: date
    ) -> Union[Any, None]:
        """Получение партии по номеру и дате (уникальная связка)"""
        pass

    async def get_by_filter(self, product_filter: TaskFilter) -> Union[List[Any], None]:
        """Получение партий по фильтру"""
        pass

    async def update(self, data: Any) -> Any:
        """Обновление партии"""
        pass

    async def create(self, task: Any) -> None:
        """Создание партии"""
        pass
