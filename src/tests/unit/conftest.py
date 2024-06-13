from uuid import UUID

import pytest
from aggregate.application.use_case.cubes import CubeCommandUseCase
from aggregate.application.use_case.products import ProductCommandUseCase
from aggregate.application.use_case.tasks import TaskCommandUseCase, TaskQueryUseCase
from dependency_injector import providers
from shared_kernel.infra.container import AppContainer

from tests.unit.fake.fake_base_orm import FakeOrmCube, FakeOrmProduct, FakeOrmTask
from tests.unit.fake.fake_uow import FakeUnitOfWork


@pytest.fixture(scope="package")
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture()
def container() -> AppContainer:
    container = AppContainer()
    container.uow.override(providers.Factory(FakeUnitOfWork))
    return container


@pytest.fixture()
def uow(container: AppContainer) -> FakeUnitOfWork:
    uow: FakeUnitOfWork = container.uow()
    yield uow
    uow.tasks.data = []
    uow.cubes.data = []
    uow.products.data = []


def delete_by_id(len_for_del: list, id: UUID) -> None:
    for i in range(len(len_for_del)):
        if len_for_del[i].id == id:
            del len_for_del[i]
            break


def create_product() -> FakeOrmProduct:
    return FakeOrmProduct(
        id="013295f6-cc00-40b0-b1a9-c31c7eb54aa4",
        product_code='product',
        is_aggregated=False,
        aggregated_at=None,
        task_id="013132f6-cc00-40b0-b1a9-c31c7eb54aa4",
    )


def put_product(uow: FakeUnitOfWork) -> FakeOrmProduct:
    rep = uow.products
    new_product = create_product()
    rep.data.append(new_product)
    yield new_product
    delete_by_id(rep.data, new_product.id)


@pytest.fixture()
def product(uow: FakeUnitOfWork) -> FakeOrmProduct:
    yield from put_product(uow)


@pytest.fixture()
def product_command_use(container: AppContainer) -> ProductCommandUseCase:
    pc = container.product_command()
    rep = pc.uow.products
    yield pc
    rep.data = []


@pytest.fixture()
def cube_command_use(container: AppContainer) -> CubeCommandUseCase:
    cc = container.cube_command()
    rep = cc.uow.cubes
    yield cc
    rep.data = []


@pytest.fixture()
def task_query_use(container: AppContainer) -> TaskQueryUseCase:
    tq = container.task_query()
    rep = tq.uow.tasks
    yield tq
    rep.data = []


@pytest.fixture()
def task_command_use(container: AppContainer) -> TaskCommandUseCase:
    tc = container.task_command()
    rep = tc.uow.tasks
    yield tc
    rep.data = []


def create_task(number: int) -> FakeOrmTask:
    return FakeOrmTask(
        id=f"0{number}3132f6-cc00-40b0-b1a9-c31c7eb54aa4",
        status_closed=False,
        shift_task_representation="string",
        line="string",
        shift="string",
        brigade="string",
        batch_number=645646,
        batch_date=f"2024-04-1{number}",
        nomenclature="string",
        code_ekn="string",
        identifier_rc="string",
        shift_start_time="2024-04-15T10:07:21",
        shift_end_time="2024-04-15T10:07:21",
        closed_at=None,
        products=[],
        cubes=[],
    )


def put_task(uow: FakeUnitOfWork) -> FakeOrmTask:
    rep = uow.tasks
    new_task = create_task(1)
    rep.data.append(new_task)
    yield new_task
    delete_by_id(rep.data, new_task.id)


@pytest.fixture()
def task(uow: FakeUnitOfWork) -> FakeOrmTask:
    yield from put_task(uow)


def create_cube() -> FakeOrmCube:
    return FakeOrmCube(
        id="013146f6-cc00-40b0-b1a9-c31c7eb54aa4",
        product_code='cube',
        is_aggregated=False,
        aggregated_at=None,
        task_id="013132f6-cc00-40b0-b1a9-c31c7eb54aa4",
    )


def put_cube(uow: FakeUnitOfWork) -> FakeOrmCube:
    rep = uow.cubes
    new_cube = create_cube()
    rep.data.append(new_cube)
    yield new_cube
    delete_by_id(rep.data, new_cube.id)


@pytest.fixture()
def cube(uow: FakeUnitOfWork) -> FakeOrmCube:
    yield from put_cube(uow)


def generate_n_task(uow: FakeUnitOfWork, n: int) -> list[FakeOrmTask]:
    rep = uow.tasks
    added_id = []
    added_task = []
    for number in range(n):
        new_task = create_task(number)
        added_id.append(new_task.id)
        rep.data.append(new_task)
        added_task.append(new_task)
    yield added_task
    for id in added_id:
        delete_by_id(rep.data, id)


@pytest.fixture()
def generate_many_task(uow: FakeUnitOfWork) -> list[FakeOrmTask]:
    yield from generate_n_task(uow, 5)
