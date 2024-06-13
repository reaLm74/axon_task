from inspect import Traceback
from typing import Type

from aggregate.infra.repository import (
    SQLACubesRepository,
    SQLAProductsRepository,
    SQLATasksRepository,
)
from sqlalchemy.ext.asyncio import async_sessionmaker

from shared_kernel.infra.uow.base import UnitOfWork


class SQLAlchemyUnitOfWork(UnitOfWork):
    """Реализация uow для алхимии"""

    def __init__(self, async_session_maker: async_sessionmaker) -> None:
        self._async_session_maker = async_session_maker

    async def __aenter__(self) -> None:
        self.session = self._async_session_maker()

        self.tasks = SQLATasksRepository(self.session)
        self.products = SQLAProductsRepository(self.session)
        self.cubes = SQLACubesRepository(self.session)

        return await super().__aenter__()

    async def __aexit__(
        self, exc_type: Type[Exception], exc: Exception, tb: Traceback
    ) -> None:
        await super().__aexit__(exc_type, exc, tb)
        await self.session.close()

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()
