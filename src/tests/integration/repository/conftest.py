from datetime import datetime
from typing import Any, AsyncGenerator, Generator

import pytest
from aggregate.domain.entity import Task, Cube, Product
from pytest_asyncio import fixture as async_fixture
from shared_kernel.infra.db.db import Base
from shared_kernel.infra.uow.base import UnitOfWork
from shared_kernel.infra.uow.sqlalchemy import SQLAlchemyUnitOfWork
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool
from testcontainers.postgres import PostgresContainer
from tests.utils.make import add_task, add_cube, add_product


@pytest.fixture(scope="session")
def db_url() -> Generator[str, Any, Any]:
    with PostgresContainer("postgres:13-alpine") as container:
        yield container.get_connection_url(driver="asyncpg")


@pytest.fixture(scope="session")
def engine(db_url: str) -> AsyncEngine:
    return create_async_engine(db_url, poolclass=NullPool)


@pytest.fixture
def session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        autoflush=False,
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )


@async_fixture(scope="function", autouse=True)
async def init_db(engine: AsyncEngine) -> AsyncGenerator[Any, None]:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
def uow(session_factory: async_sessionmaker[AsyncSession]) -> UnitOfWork:
    return SQLAlchemyUnitOfWork(session_factory)


def create_task(number: int) -> Task:
    return Task(
        status_closed=False,
        shift_task_representation="string",
        line="string",
        shift="string",
        brigade="string",
        batch_number=645646,
        batch_date=datetime.strptime(f"2024-04-1{number}", "%Y-%m-%d"),
        nomenclature="string",
        code_ekn="string",
        identifier_rc="string",
        shift_start_time="2024-04-15T10:07:21",
        shift_end_time="2024-04-15T10:07:21"
    )


@pytest.fixture()
def update_data() -> Task:
    return Task(
        status_closed=True,
        shift_task_representation="11111",
        line="111111",
        shift="1111111",
        brigade="111111",
        batch_number=634736,
        batch_date=datetime.strptime("2024-04-02", "%Y-%m-%d"),
        nomenclature="111111",
        code_ekn="111111",
        identifier_rc="111111",
        shift_start_time="2024-04-15T10:07:21",
        shift_end_time="2024-04-15T10:07:21",
        closed_at=None
    )


@pytest.fixture()
def generate_many_task() -> list[Task]:
    return [create_task(i) for i in range(5)]


@async_fixture
async def task(uow: UnitOfWork) -> Task:
    return await add_task(uow)


@async_fixture
async def cube(uow: UnitOfWork, task: Task) -> Cube:
    return await add_cube(uow, task)


@async_fixture
async def product(uow: UnitOfWork, task: Task) -> Product:
    return await add_product(uow, task)
