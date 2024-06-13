from shared_kernel.infra.uow.base import UnitOfWork

from aggregate.application.use_case.items import ItemsCommandUseCase
from aggregate.domain.entity import Cube


class CubeCommandUseCase(ItemsCommandUseCase):
    def __init__(self, uow: UnitOfWork):
        super().__init__(uow=uow, repo="cubes", entity=Cube)
