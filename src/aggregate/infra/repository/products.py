from shared_kernel.infra.db.orm import ProductTable
from sqlalchemy.ext.asyncio import AsyncSession

from aggregate.infra.repository.abstract import ProductsRepository

from .items import SQLAItemsRepository


class SQLAProductsRepository(SQLAItemsRepository, ProductsRepository):
    """Репозиторий для продуктов"""

    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=ProductTable)
