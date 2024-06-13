from shared_kernel.infra.db.orm import CubesTable
from sqlalchemy.ext.asyncio import AsyncSession

from aggregate.infra.repository.abstract import CubesRepository

from .items import SQLAItemsRepository


class SQLACubesRepository(SQLAItemsRepository, CubesRepository):
    """Репозиторий для кубов"""

    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=CubesTable)
