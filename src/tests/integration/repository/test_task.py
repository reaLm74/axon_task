from aggregate.infra.filter import TaskFilter
from pytest import mark
from shared_kernel.infra.uow.base import UnitOfWork
from aggregate.domain.entity import Task


@mark.asyncio
async def test_add_many_tasks(uow: UnitOfWork, generate_many_task: list[Task]) -> None:
    async with uow:
        for task in generate_many_task:
            await uow.tasks.create(task)
        await uow.commit()
        list_task = await uow.tasks.get_by_filter(TaskFilter())
        assert len(list_task) == len(generate_many_task)


@mark.asyncio
async def test_filter(uow: UnitOfWork, task: Task) -> None:
    async with uow:
        product_filter = TaskFilter(status_closed=False)
        get_task = await uow.tasks.get_by_filter(product_filter)
        assert get_task[0].id == task.id


@mark.asyncio
async def test_get_task_by_num_date(uow: UnitOfWork, task: Task) -> None:
    async with uow:
        result = await uow.tasks.get_by_num_date(
            batch_number=task.batch_number,
            batch_date=task.batch_date
        )
        assert result.id == task.id


@mark.asyncio
async def test_get_task_by_id(uow: UnitOfWork, task: Task) -> None:
    async with uow:
        result = await uow.tasks.get_by_id(task_id=task.id)
        assert result.id == task.id


@mark.asyncio
async def test_update_task(uow: UnitOfWork, task: Task, update_data: Task) -> None:
    async with uow:
        result = await uow.tasks.get_by_id(task_id=task.id)
        await uow.tasks.update(data=update_data)
        result_update = await uow.tasks.get_by_id(task_id=task.id)
        assert result_update != result
        assert result_update.line == update_data.line
