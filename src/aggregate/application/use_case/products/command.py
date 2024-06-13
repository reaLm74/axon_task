from shared_kernel.infra.uow.base import UnitOfWork

from aggregate.application.use_case.items import ItemsCommandUseCase
from aggregate.domain.entity import Product


class ProductCommandUseCase(ItemsCommandUseCase):
    def __init__(self, uow: UnitOfWork):
        super().__init__(uow=uow, repo="products", entity=Product)
