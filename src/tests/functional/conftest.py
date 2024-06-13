import asyncio
from typing import Any, AsyncGenerator

import pytest
from async_asgi_testclient import TestClient
from fastapi import FastAPI
from pytest_asyncio import fixture as async_fixture
from shared_kernel.infra.db.db import Base
from shared_kernel.infra.uow.base import UnitOfWork
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from testcontainers.postgres import PostgresContainer

from aggregate.domain.entity import Cube, Product, Task
from tests.utils.make import add_cube, add_product, add_task


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def db_url():
    with PostgresContainer(
            "postgres:13-alpine", username="postgres", password="postgres",
            dbname="postgres"
    ).with_bind_ports(5432, 5432) as container:
        yield container.get_connection_url(driver="asyncpg")


@pytest.fixture(scope="session")
def engine(db_url: str) -> AsyncEngine:
    return create_async_engine(db_url)


@async_fixture(scope="function", autouse=True)
async def init_db(engine: AsyncEngine) -> AsyncGenerator[Any, None]:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="session")
def app():
    from shared_kernel.infra.fastapi.main import app
    return app


@async_fixture(scope="session")
async def client(app):
    async with TestClient(app) as client:
        yield client


@pytest.fixture
def uow(app: FastAPI) -> UnitOfWork:
    return app.container.uow()  # type: ignore


@async_fixture
async def task(uow: UnitOfWork) -> Task:
    return await add_task(uow)


@async_fixture
async def cube(uow: UnitOfWork, task: Task) -> Cube:
    return await add_cube(uow, task)


@async_fixture
async def product(uow: UnitOfWork, task: Task) -> Product:
    return await add_product(uow, task)
