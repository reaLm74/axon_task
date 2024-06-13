import uuid
from typing import Any, Union

from aggregate.infra.repository.abstract import ProductsRepository

from tests.unit.fake.fake_base_orm import FakeOrmProduct


class FakeProductRepository(ProductsRepository):
    _data: list[FakeOrmProduct] = []

    @property
    def data(self) -> list[FakeOrmProduct]:
        return FakeProductRepository._data

    @data.setter
    def data(self, new_data: list[FakeOrmProduct]) -> None:
        FakeProductRepository._data = new_data

    async def get_by_code(self, product_code: str) -> Union[Any, None]:
        """
        Поиск по уникальному коду
        """
        for item in self.data:
            if item.product_code == product_code:
                return item
        return None

    async def get_by_id_code(self, field_item_search: Any) -> Union[Any, None]:
        """
        Поиск по id партии и уникальному коду
        """
        for item in self.data:
            if (
                    item.product_code == field_item_search.product_code
            ) and (
                    item.task_id == field_item_search.task_id
            ):
                return item
        return None
        pass

    async def create(self, field_item: Any) -> None:
        """
        Создание
        """
        dump_item = field_item.model_dump()
        dump_item["id"] = uuid.uuid4()
        dump_item["is_aggregated"] = False
        dump_item["aggregated_at"] = None
        new_item = FakeOrmProduct(**dump_item)
        self.data.append(new_item)

    async def update(self, item: Any) -> None:
        pass
