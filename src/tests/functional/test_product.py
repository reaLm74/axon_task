from random import randint

from fastapi import status
from httpx import AsyncClient
from pytest import mark

from aggregate.domain.entity import Product, Task

num = randint(1000, 99999999)


@mark.asyncio
async def test_add_product(client: AsyncClient, task: Task) -> None:
    """Добавление продукта"""
    data_product = [
        {
            "УникальныйКод": f"{num}",
            "НомерПартии": task.batch_number,
            "ДатаПартии": str(task.batch_date),
        },
    ]
    response = await client.post("/products/add", json=data_product)
    assert response.status_code == status.HTTP_201_CREATED


@mark.asyncio
async def test_aggregate_product_id(
        client: AsyncClient,
        product: Product
) -> None:
    """Аггрегирование / деагрегирование"""

    aggregate = {
        "task_id": str(product.task_id),
        "product_code": str(product.product_code)
    }
    response = await client.patch("/products/aggregate/by_batch_id", json=aggregate)
    assert response.status_code == status.HTTP_201_CREATED
    response = await client.patch("/products/deaggregate/by_batch_id", json=aggregate)
    assert response.status_code == status.HTTP_201_CREATED


@mark.asyncio
async def test_aggregate_product_date_number(
        client: AsyncClient,
        task: Task,
        product: Product
) -> None:
    """Аггрегирование / деагрегирование дата номер"""

    aggregate = {
        "batch_date": str(task.batch_date),
        "batch_number": task.batch_number,
        "product_code": product.product_code,
    }
    response = await client.patch(
        "/products/aggregate/by_batch_datenumber", json=aggregate
    )
    assert response.status_code == status.HTTP_201_CREATED
    response = await client.patch(
        "/products/deaggregate/by_batch_datenumber", json=aggregate
    )
    assert response.status_code == status.HTTP_201_CREATED


@mark.asyncio
async def test_search_product_id(
        client: AsyncClient,
        product: Product
) -> None:
    """Поиск по id"""

    aggregate = {"task_id": str(product.task_id), "product_code": product.product_code}
    response = await client.patch("/products/search/by_batch_id", json=aggregate)
    assert response.status_code == status.HTTP_200_OK


@mark.asyncio
async def test_search_product_date_number(
        client: AsyncClient,
        task: Task,
        product: Product
) -> None:
    """Поиск по дате номеру"""

    aggregate = {
        "batch_date": str(task.batch_date),
        "batch_number": task.batch_number,
        "product_code": product.product_code,
    }
    response = await client.patch(
        "/products/search/by_batch_datenumber",
        json=aggregate
    )
    assert response.status_code == status.HTTP_200_OK
