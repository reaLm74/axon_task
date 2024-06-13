from random import randint

from fastapi import status
from httpx import AsyncClient
from pydantic import TypeAdapter
from pytest import mark

from aggregate.domain.entity import Task

from .data import data, update

num = randint(1000, 99999999)


@mark.asyncio
async def test_add_task(client: AsyncClient) -> None:
    response = await client.post("/tasks/add", json=data)
    assert response.status_code == status.HTTP_201_CREATED


@mark.asyncio
async def test_update_task(
        client: AsyncClient,
        task: Task,
        update_in: dict = update
) -> None:
    response_task = await client.patch(f"/tasks/{task.id}", json=update_in)
    assert response_task.status_code == status.HTTP_201_CREATED
    actual_task = Task.model_validate(response_task.json())
    assert actual_task.closed_at


@mark.asyncio
async def test_tasks(client: AsyncClient, task: Task) -> None:
    response = await client.get(
        "/tasks?page=0&size=2&status_closed=false&order_by=batch_number"
    )
    assert response.status_code == status.HTTP_200_OK
    actual_batches = TypeAdapter(list[Task]).validate_python(response.json()["data"])
    assert [task] == actual_batches


@mark.asyncio
async def test_one_task(client: AsyncClient, task: Task) -> None:
    response_task = await client.get(f"/tasks/{task.id}")
    assert response_task.status_code == status.HTTP_200_OK

