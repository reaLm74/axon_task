from typing import Type

from shared_kernel.infra.uow.base import UnitOfWork

from aggregate.application.dto import (
    AddItem,
    AggregateDataNumberItem,
    AggregateIdItem,
    FieldSearchItem,
    ItemResponse,
    SearchDataNumberItem,
    SearchIdItem,
)
from aggregate.domain.entity import Cube, Item, Product, Task
from aggregate.domain.exceptions import (
    ErrorCodeAttached,
    ErrorCodeUsed,
    ErrorProductDeaggregate,
    ItemNotFound,
    TaskClosed,
    TaskNotFound,
)


class ItemsCommandUseCase:
    def __init__(self, uow: UnitOfWork, repo: str, entity: Type[Item]):
        self.uow = uow
        self.repo = repo
        self.entity = entity

    async def add(self, items: list[AddItem]) -> None:
        async with self.uow as uow:
            for item in items:
                task: Task | None = await uow.tasks.get_by_num_date(
                    batch_number=item.batch_number, batch_date=item.batch_date
                )
                if task is None or task.status_closed:
                    continue
                repo = getattr(uow, self.repo)
                check_item: Cube | Product | None = await repo.get_by_code(
                    product_code=item.product_code
                )
                if check_item is None:
                    create_item = self.entity(
                        product_code=item.product_code,
                        task_id=task.id,  # type: ignore
                    )
                    await repo.create(create_item)
            await uow.commit()

    async def aggregate(
        self, aggregation: AggregateIdItem | AggregateDataNumberItem
    ) -> ItemResponse:
        async with self.uow as uow:
            if hasattr(aggregation, "task_id"):
                task: Task | None = await uow.tasks.get_by_id(
                    task_id=aggregation.task_id
                )
            else:
                task = await uow.tasks.get_by_num_date(
                    batch_number=aggregation.batch_number,
                    batch_date=aggregation.batch_date,
                )
            if task is None:
                raise TaskNotFound()
            if task.status_closed:
                raise TaskClosed()
            repo = getattr(uow, self.repo)
            item: Cube | Product | None = await repo.get_by_code(
                product_code=aggregation.product_code
            )
            if item is None:
                raise ItemNotFound()
            if item.task_id != task.id:
                raise ErrorCodeAttached()
            if item.is_aggregated:
                raise ErrorCodeUsed(item.aggregated_at)  # type: ignore
            item.aggregated(self.repo)
            await repo.update(item=item)
            await uow.commit()
            item_response = ItemResponse.model_validate(item, from_attributes=True)
            return item_response

    async def deaggregate(
        self, aggregation: AggregateIdItem | AggregateDataNumberItem
    ) -> ItemResponse:
        async with self.uow as uow:
            if hasattr(aggregation, "task_id"):
                task: Task | None = await uow.tasks.get_by_id(
                    task_id=aggregation.task_id
                )
            else:
                task = await uow.tasks.get_by_num_date(
                    batch_number=aggregation.batch_number,
                    batch_date=aggregation.batch_date,
                )
            if task is None:
                raise TaskNotFound()
            if task.status_closed:
                raise TaskClosed()
            repo = getattr(uow, self.repo)
            item: Cube | Product | None = await repo.get_by_code(
                product_code=aggregation.product_code
            )
            if item is None:
                raise ItemNotFound()
            if item.task_id != task.id:
                raise ErrorCodeAttached()
            if not item.is_aggregated:
                raise ErrorProductDeaggregate()
            item.deaggregated(self.repo)
            await repo.update(item=item)
            await uow.commit()
            item_response = ItemResponse.model_validate(item, from_attributes=True)
            return item_response

    async def search(self, search: SearchIdItem | SearchDataNumberItem) -> ItemResponse:
        async with self.uow as uow:
            if hasattr(search, "task_id"):
                task_id = search.task_id
            else:
                task: Task = await uow.tasks.get_by_num_date(
                    batch_number=search.batch_number,
                    batch_date=search.batch_date,
                )
                if task is None:
                    raise TaskNotFound()
                task_id = task.id
            repo = getattr(uow, self.repo)
            field_item_search = FieldSearchItem(
                product_code=search.product_code, task_id=task_id
            )
            item: Cube | Product | None = await repo.get_by_id_code(field_item_search)
            if item is None:
                raise ItemNotFound()
            item_response = ItemResponse.model_validate(item, from_attributes=True)
            return item_response
