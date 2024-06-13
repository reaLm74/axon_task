from random import randint

from fastapi import status
from httpx import AsyncClient
from pytest import mark

from aggregate.domain.entity import Cube, Task

num = randint(1000, 99999999)


@mark.asyncio
async def test_add_cube(client: AsyncClient, task: Task) -> None:
    """Добавление куба"""

    data_cubes = [
        {
            "УникальныйКод": f"{num}",
            "НомерПартии": task.batch_number,
            "ДатаПартии":  str(task.batch_date),
        },
    ]
    response = await client.post("/cubes/add", json=data_cubes)
    assert response.status_code == status.HTTP_201_CREATED


@mark.asyncio
async def test_aggregate_cube_id(client: AsyncClient, cube: Cube) -> None:
    """Аггрегирование / деагрегирование"""

    aggregate = {"task_id": str(cube.task_id), "product_code": str(cube.product_code)}
    response = await client.patch("/cubes/aggregate/by_batch_id", json=aggregate)
    assert response.status_code == status.HTTP_201_CREATED
    response = await client.patch("/cubes/deaggregate/by_batch_id", json=aggregate)
    assert response.status_code == status.HTTP_201_CREATED


@mark.asyncio
async def test_aggregate_cube_date_number(
        client: AsyncClient,
        task: Task,
        cube: Cube
) -> None:
    """Аггрегирование / деагрегирование дата номер"""

    aggregate = {
        "batch_date": str(task.batch_date),
        "batch_number": task.batch_number,
        "product_code": cube.product_code,
    }
    response = await client.patch(
        "/cubes/aggregate/by_batch_datenumber", json=aggregate
    )
    assert response.status_code == status.HTTP_201_CREATED
    response = await client.patch(
        "/cubes/deaggregate/by_batch_datenumber", json=aggregate
    )
    assert response.status_code == status.HTTP_201_CREATED


@mark.asyncio
async def test_search_cube_id(
        client: AsyncClient,
        cube: Cube
) -> None:
    """Поиск по id"""

    aggregate = {"task_id": str(cube.task_id), "product_code": cube.product_code}
    response = await client.patch("/cubes/search/by_batch_id", json=aggregate)
    assert response.status_code == status.HTTP_200_OK


@mark.asyncio
async def test_search_cube_date_number(
        client: AsyncClient,
        task: Task,
        cube: Cube
) -> None:
    """Поиск по дате номеру"""

    aggregate = {
        "batch_date": str(task.batch_date),
        "batch_number": task.batch_number,
        "product_code": cube.product_code,
    }
    response = await client.patch("/cubes/search/by_batch_datenumber", json=aggregate)
    assert response.status_code == status.HTTP_200_OK
