from datetime import datetime
from typing import List

from fastapi import HTTPException
from fastapi import status
from sqlalchemy import and_
from sqlalchemy import select

from app.db.db import async_session_maker
from app.models.products import ProductTable
from app.models.tasks import TaskTable
from app.schemas.aggregate import Aggregation
from app.schemas.products import Product


async def add_product(new_products: List[Product]):
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


async def aggregate_product(aggregation: Aggregation):
    async with async_session_maker() as session:
        query_task = (
            select(TaskTable).filter(TaskTable.id == aggregation.task_id)
        )
        task = await session.scalar(query_task)
        if task is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST
            )
        if task.status_closed:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST
            )
        query = (
            select(ProductTable).filter(
                ProductTable.product_code == aggregation.product_code
            )
        )
        product = await session.scalar(query)
        if product is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST
            )
        if product.task_id != aggregation.task_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST
            )
        if product.is_aggregated:
            date = product.aggregated_at.strftime("%H:%M:%S %d.%m.%Y")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST
            )
        setattr(product, 'is_aggregated', True)
        setattr(product, 'aggregated_at', datetime.now())
        await session.commit()
        return {'product_code': product.product_code}
