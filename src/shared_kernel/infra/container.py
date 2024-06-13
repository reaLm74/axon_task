from aggregate.application.use_case.cubes import CubeCommandUseCase
from aggregate.application.use_case.products import ProductCommandUseCase
from aggregate.application.use_case.tasks import (
    TaskCommandUseCase,
    TaskQueryUseCase,
)
from dependency_injector import containers, providers

from shared_kernel.infra.uow.base import UnitOfWork


class AppContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "aggregate.presentation.rest.tasks",
            "aggregate.presentation.rest.products",
            "aggregate.presentation.rest.cubes",
        ]
    )
    uow = providers.AbstractFactory(UnitOfWork)

    task_query = providers.Factory(TaskQueryUseCase, uow=uow)
    task_command = providers.Factory(TaskCommandUseCase, uow=uow)
    product_command = providers.Factory(ProductCommandUseCase, uow=uow)
    cube_command = providers.Factory(CubeCommandUseCase, uow=uow)
