from opentelemetry import trace
from shared_kernel.infra.db.data_mappers import item_to_model
from shared_kernel.infra.fastapi.meter import record_total
from sqlalchemy import and_, select

from aggregate.application.dto import FieldSearchItem
from aggregate.domain.entity import Cube, Product
from aggregate.infra.repository import SQLABaseRepository
from aggregate.infra.repository.abstract import ItemsRepository

tracer = trace.get_tracer(__name__)


class SQLAItemsRepository(SQLABaseRepository, ItemsRepository):
    """Базовый репозиторий для выпускаемой продукции"""

    async def get_by_code(self, product_code: str) -> Cube | Product | None:
        """Поиск по уникальному коду"""

        with tracer.start_as_current_span(f"sqlalchemy.{self.name}.get_by_id"):
            query = select(self.model).filter(self.model.product_code == product_code)
            result = await self.session.scalar(query)
            if result is None:
                return None
            self._identity_map["item"] = result
            entity: Cube | Product = await item_to_model(result, self.name)
            return entity

    async def get_by_id_code(
        self, field_item_search: FieldSearchItem
    ) -> Cube | Product | None:
        """Поиск по id партии и уникальному коду"""

        with tracer.start_as_current_span(f"sqlalchemy.{self.name}.get_by_id"):
            query = select(self.model).filter(
                and_(
                    self.model.task_id == field_item_search.task_id,
                    self.model.product_code == field_item_search.product_code,
                )
            )
            result = await self.session.scalar(query)
            if result is None:
                return None
            entity: Cube | Product = await item_to_model(result, self.name)
            return entity

    async def create(self, create_item: Cube | Product) -> None:
        """Создание продукции"""

        instance = self.model(**create_item.model_dump())
        self.session.add(instance)
        record_total(self.name)

    async def update(self, item: Cube | Product) -> None:
        """Обновление продукции"""

        old_item = self._identity_map["item"]
        patch_dict = item.model_dump(exclude_unset=True)
        for key, value in patch_dict.items():
            setattr(old_item, key, value)
        self.session.add(old_item)
