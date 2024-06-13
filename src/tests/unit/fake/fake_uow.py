from typing import Any

from shared_kernel.infra.uow.base import UnitOfWork

from . import FakeCubesRepository, FakeProductRepository, FakeTasksRepository


class FakeUnitOfWork(UnitOfWork):
    def __init__(self) -> None:
        self.tasks = FakeTasksRepository()
        self.cubes = FakeCubesRepository()
        self.products = FakeProductRepository()

    async def __aenter__(self) -> Any:
        self.old_tasks_data = self.tasks.data.copy()
        self.old_cubes_data = self.cubes.data.copy()
        self.old_products_data = self.products.data.copy()
        return await super().__aenter__()

    async def commit(self) -> None:
        self.old_tasks_data = self.tasks.data.copy()
        self.old_cubes_data = self.cubes.data.copy()
        self.old_products_data = self.products.data.copy()

    async def rollback(self) -> None:
        self.tasks.data = self.old_tasks_data.copy()
        self.cubes.data = self.old_cubes_data.copy()
        self.products.data = self.old_products_data.copy()
