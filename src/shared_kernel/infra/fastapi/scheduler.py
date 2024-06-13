import logging
from datetime import datetime, timedelta, timezone

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import and_, select

from shared_kernel.infra.db.db import async_session_maker
from shared_kernel.infra.db.orm import TaskTable
from shared_kernel.infra.fastapi.config import settings as config

logger = logging.getLogger("api")


async def check_date_task() -> None:
    async with async_session_maker() as session:
        query = select(TaskTable).filter(
            and_(
                datetime.now(timezone.utc)
                + timedelta(minutes=config.TIMEDELTA_MINUTES_MIN)
                < TaskTable.shift_start_time,
                datetime.now(timezone.utc)
                + timedelta(minutes=config.TIMEDELTA_MINUTES_MAX)
                > TaskTable.shift_start_time,
            )
        )
        result = await session.scalars(query)
        tasks = result.all()
        if len(tasks) > 1:
            logger.warning("Одновременное начало нескольких партий")
        for task in tasks:
            logger.info(
                f"Партия № {task.batch_number}, {task.batch_date} "
                f"должна начаться в {task.shift_start_time}"
            )


def run_scheduler() -> None:
    scheduler = AsyncIOScheduler()
    scheduler.add_job(check_date_task, "cron", hour="*", minute="00")
    scheduler.start()
