from typing import TypeVar

from aggregate.domain.entity import Cube, Product, Task

from shared_kernel.infra.db.orm import TaskTable

_ORMType = TypeVar("_ORMType")


async def item_to_model(item: _ORMType, name_item: str) -> Cube | Product:
    """Приведение к бизнес-модели UploadedItem"""
    if name_item == "cubes":
        return Cube.model_validate(item, from_attributes=True)
    else:
        return Product.model_validate(item, from_attributes=True)


async def task_to_model(task: TaskTable) -> Task:
    """Приведение к бизнес-модели UploadedTask"""
    return Task.model_validate(task, from_attributes=True)
