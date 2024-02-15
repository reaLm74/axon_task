from random import randint

import pytest
from httpx import AsyncClient

from tests.data import data, update

num = randint(1000, 99999999)


@pytest.mark.anyio
async def test_add_task(client: AsyncClient):
    response = await client.post("/tasks/add", json=data)
    assert response.status_code == 201


@pytest.mark.anyio
async def test_update_task(client: AsyncClient):
    response = await client.patch("/tasks/1", json=update)
    assert response.status_code == 201


@pytest.mark.anyio
async def test_tasks(client: AsyncClient):
    response = await client.get(
        "/tasks?page=0&size=2&status_closed=false&order_by=batch_number"
    )
    assert response.status_code == 200


@pytest.mark.anyio
async def test_one_task(client: AsyncClient):
    response = await client.get("/tasks/1")
    assert response.status_code == 200


@pytest.mark.anyio
async def test_add_product(client: AsyncClient):
    response = await client.get("/tasks/1")
    batch_number = response.json()['batch_number']
    batch_date = response.json()['batch_date']
    data_product = [
        {
            "УникальныйКодПродукта": f"{num}",
            "НомерПартии": batch_number,
            "ДатаПартии": batch_date
        }
    ]
    response = await client.post("/products/add", json=data_product)
    assert response.status_code == 201


@pytest.mark.anyio
async def test_aggregate_product(client: AsyncClient):
    aggregate = {"task_id": 1, "product_code": f"{num}"}

    response = await client.patch("/products/aggregate", json=aggregate)
    assert response.status_code == 201
