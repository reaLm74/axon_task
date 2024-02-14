from datetime import datetime

from fastapi import HTTPException
from fastapi import status
from sqlalchemy import and_
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db.db import async_session_maker
from app.models.tasks import TaskTable
from app.schemas.tasks import ShiftTask


async def get_task(task_id: int):
    async with async_session_maker() as session:
        query = (
            select(TaskTable)
            .filter(TaskTable.id == task_id)
            .options(selectinload(TaskTable.products))
        )
        task = await session.scalar(query)
        if task is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST
            )
        return task


async def filter_task(product_filter):
    async with async_session_maker() as session:
        query = product_filter.filter(
            select(TaskTable).options(selectinload(TaskTable.products))
        )
        query_sort = product_filter.sort(query)
        result = await session.execute(query_sort)
        return result.scalars().all()


async def add_task(new_tasks):
    async with async_session_maker() as session:
        for task in new_tasks:
            query = select(TaskTable).filter(
                and_(
                    TaskTable.batch_number == task.batch_number,
                    TaskTable.batch_date == task.batch_date,
                )
            )
            old_task = await session.scalar(query)
            if old_task is not None:
                await session.delete(old_task)
                await session.commit()
            new_batch = TaskTable(**task.model_dump())
            session.add(new_batch)
        await session.commit()


async def update_task(task_id: int, update: ShiftTask):
    async with async_session_maker() as session:
        update_data = update.model_dump(exclude_unset=True)
        query = (
            select(TaskTable)
            .filter(TaskTable.id == task_id)
            .options(selectinload(TaskTable.products))
        )
        task_old = await session.scalar(query)
        if task_old is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST
            )

        if (
                "status_closed" in update_data
                and update_data["status_closed"] != task_old.status_closed
        ):
            if update_data["status_closed"]:
                task_old.closed_at = datetime.now()
            else:
                task_old.closed_at = None
        for key, value in update_data.items():
            setattr(task_old, key, value)
        await session.commit()
        return task_old
