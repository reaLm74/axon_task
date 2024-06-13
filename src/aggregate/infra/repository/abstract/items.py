from typing import Any, Union

from .base import BaseRepository


class ItemsRepository(BaseRepository):
    """Базовый репозиторий для выпускаемой продукции"""

    async def get_by_code(self, product_code: str) -> Union[Any, None]:
        """
        Поиск по уникальному коду
        """
        pass

    async def get_by_id_code(self, field_item_search: Any) -> Union[Any, None]:
        """
        Поиск по id партии и уникальному коду
        """
        pass

    async def create(self, field_item: Any) -> None:
        """
        Создание
        """
        pass

    async def update(self, item: Any) -> None:
        pass
