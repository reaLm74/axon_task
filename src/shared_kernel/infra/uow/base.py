from abc import ABC, abstractmethod
from inspect import Traceback
from typing import Any, Type

from aggregate.infra.repository import (
    SQLACubesRepository,
    SQLAProductsRepository,
    SQLATasksRepository,
)


class UnitOfWork(ABC):
    """Базовый класс uow"""

    tasks: SQLATasksRepository
    products: SQLAProductsRepository
    cubes: SQLACubesRepository

    async def __aenter__(self) -> Any:
        return self

    async def __aexit__(
        self, exc_type: Type[Exception], exc: Exception, tb: Traceback
    ) -> None:
        await self.rollback()

    @abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def rollback(self) -> None:
        raise NotImplementedError
