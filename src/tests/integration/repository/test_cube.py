from aggregate.application.dto import FieldSearchItem
from pytest import mark
from shared_kernel.infra.uow.base import UnitOfWork
from aggregate.domain.entity import Task, Cube


@mark.asyncio
async def test_add_cube(uow: UnitOfWork, task: Task) -> None:
    async with uow:
        cube = Cube(task_id=task.id, product_code="string")
        await uow.cubes.create(cube)
        await uow.commit()
        result_cube_by_code = await uow.cubes.get_by_code(cube.product_code)
        assert result_cube_by_code.task_id == task.id


@mark.asyncio
async def test_product_get_code(uow: UnitOfWork, cube: Cube) -> None:
    async with uow:
        result = await uow.cubes.get_by_code(cube.product_code)
        assert result.product_code == cube.product_code


@mark.asyncio
async def test_product_id_code(uow: UnitOfWork, cube: Cube) -> None:
    async with uow:
        search = FieldSearchItem(
            task_id=cube.task_id,
            product_code=cube.product_code
        )
        result = await uow.cubes.get_by_id_code(field_item_search=search)
        assert result.product_code == cube.product_code


@mark.asyncio
async def test_product_aggregated(uow: UnitOfWork, cube: Cube) -> None:
    async with uow:
        get_product = await uow.cubes.get_by_code(cube.product_code)
        get_product.aggregated()
        await uow.cubes.update(get_product)
        await uow.commit()
        result_update = await uow.cubes.get_by_code(cube.product_code)
        assert result_update.is_aggregated is True
