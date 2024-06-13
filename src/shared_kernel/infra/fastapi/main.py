from contextlib import asynccontextmanager
from typing import AsyncGenerator

import uvicorn
from dependency_injector import providers
from fastapi import FastAPI

from shared_kernel.infra.container import AppContainer
from shared_kernel.infra.db.db import async_session_maker
from shared_kernel.infra.fastapi.logger import create_logger
from shared_kernel.infra.fastapi.routers import all_routers
from shared_kernel.infra.fastapi.scheduler import run_scheduler
from shared_kernel.infra.uow.sqlalchemy import SQLAlchemyUnitOfWork


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    run_scheduler()
    yield


def create_app() -> FastAPI:
    app = FastAPI(title="aggregate", lifespan=lifespan)
    create_logger()
    for router in all_routers:
        app.include_router(router)
    app_container = AppContainer()
    app_container.uow.override(
        providers.Factory(SQLAlchemyUnitOfWork, async_session_maker)
    )
    app.container = app_container  # type: ignore
    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)  # noqa
