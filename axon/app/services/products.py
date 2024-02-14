from abc import ABC, abstractmethod
from datetime import datetime
from typing import List

from sqlalchemy import and_
from sqlalchemy import select

from app.db.db import async_session_maker
from app.models.products import ProductTable
from app.models.tasks import TaskTable
from app.schemas.aggregate import Aggregation
from app.schemas.products import Product
from app.utils.exception import (ProductNotExist, ErrorCodeAttached, BatchNone,
                                 ErrorCodeUsed, BatchClosed)


class AbstractRepository(ABC):
    @abstractmethod
    async def add_product(self, new_products: List[Product]):
        raise NotImplementedError

    @abstractmethod
    async def aggregate_product(self, aggregation: Aggregation):
        raise NotImplementedError


class ProductRepository(AbstractRepository):
    async def add_product(self, new_products: List[Product]):
        async with async_session_maker() as session:
            for product in new_products:
                query = (
                    select(TaskTable).filter(and_(
                        TaskTable.batch_number == product.batch_number,
                        TaskTable.batch_date == product.batch_date,
                    ))
                )
                task = await session.scalar(query)
                if task is None or task.status_closed:
                    continue
                create_product = ProductTable(
                    product_code=product.product_code,
                    task_id=task.id
                )
                session.add(create_product)
            await session.commit()

    async def aggregate_product(self, aggregation: Aggregation):
        async with async_session_maker() as session:
            query_task = (
                select(TaskTable).filter(TaskTable.id == aggregation.task_id)
            )
            task = await session.scalar(query_task)
            if task is None:
                raise BatchNone()
            if task.status_closed:
                raise BatchClosed()
            query = (
                select(ProductTable).filter(
                    ProductTable.product_code == aggregation.product_code
                )
            )
            product = await session.scalar(query)
            if product is None:
                raise ProductNotExist()
            if product.task_id != aggregation.task_id:
                raise ErrorCodeAttached()
            if product.is_aggregated:
                date = product.aggregated_at.strftime("%H:%M:%S %d.%m.%Y")
                raise ErrorCodeUsed(date)
            setattr(product, 'is_aggregated', True)
            setattr(product, 'aggregated_at', datetime.now())
            await session.commit()
            return {'product_code': product.product_code}
