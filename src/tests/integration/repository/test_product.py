from aggregate.application.dto import FieldSearchItem
from pytest import mark
from shared_kernel.infra.uow.base import UnitOfWork
from aggregate.domain.entity import Task, Product


@mark.asyncio
async def test_add_product(uow: UnitOfWork, task: Task) -> None:
    async with uow:
        product = Product(task_id=task.id, product_code="string")
        await uow.products.create(product)
        await uow.commit()
        result_product_by_code = await uow.products.get_by_code(product.product_code)
        assert result_product_by_code.task_id == task.id


@mark.asyncio
async def test_product_get_code(uow: UnitOfWork, product: Product) -> None:
    async with uow:
        result = await uow.products.get_by_code(product.product_code)
        assert result.product_code == product.product_code


@mark.asyncio
async def test_product_id_code(uow: UnitOfWork, product: Product) -> None:
    async with uow:
        search = FieldSearchItem(
            task_id=product.task_id,
            product_code=product.product_code
        )
        result = await uow.products.get_by_id_code(field_item_search=search)
        assert result.product_code == product.product_code


@mark.asyncio
async def test_product_aggregated(uow: UnitOfWork, product: Product) -> None:
    async with uow:
        get_product = await uow.products.get_by_code(product.product_code)
        get_product.aggregated()
        await uow.products.update(get_product)
        await uow.commit()
        result_update = await uow.products.get_by_code(product.product_code)
        assert result_update.is_aggregated is True
