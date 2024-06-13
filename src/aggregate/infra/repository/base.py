from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from aggregate.infra.repository.abstract import BaseRepository


class SQLABaseRepository(BaseRepository):
    """Базовый репозиторий для продуктов и кубов"""

    def __init__(self, session: AsyncSession, model: Any):
        self.session = session
        self.model = model
        self.name = self.model.__tablename__
        self._identity_map: dict[str, Any] = dict()
