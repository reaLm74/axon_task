import uuid

import pytest
from aggregate.application.dto import FilterData, TaskResponse, TaskUpdate
from aggregate.domain.exceptions import TaskNotFound

from tests.unit.fake.fake_base_orm import FakeAddTask


@pytest.mark.anyio
async def test_task_get_by_id(task_query_use, task) -> None:
    result = await task_query_use.get_by_id(task.id)
    assert result == TaskResponse.model_validate(task, from_attributes=True)


@pytest.mark.anyio
async def test_task_get_by_id_wrong_id(task_query_use) -> None:
    with pytest.raises(TaskNotFound):
        await task_query_use.get_by_id(uuid.uuid4())


@pytest.mark.anyio
async def test_task_get_by_num_date(task_query_use, task) -> None:
    result = await task_query_use.get_by_num_date(task.batch_number, task.batch_date)
    assert result == TaskResponse.model_validate(task, from_attributes=True)


@pytest.mark.anyio
async def test_task_get_by_num_date_wrong_id(task_query_use) -> None:
    with pytest.raises(TaskNotFound):
        await task_query_use.get_by_num_date(000000, "2000-04-15")


@pytest.mark.parametrize(
    "page, size, filter_data, result_len, total",
    [
        pytest.param(0, 2, {}, 2, 2, id="no_filter_2_task"),
        pytest.param(0, 1, {}, 1, 4, id="no_filter_1_task"),
        pytest.param(0, 5, {}, 5, 0, id="no_filter_5_task"),
        pytest.param(0, 2, {'status_closed': 'false'}, 2, 2, id="status_closed_false"),
        pytest.param(0, 2, {'status_closed': 'false', 'batch_date': '2024-04-11'}, 1, 0,
                     id="status_closed_false_batch_date_2024-04-11"),
        pytest.param(0, 2, {'status_closed': 'true'}, 0, -1, id="status_closed_true"),
        pytest.param(0, 2, {'shift_task_representation': 'string'}, 2, 2,
                     id="shift_task_representation_string"),
        pytest.param(0, 2, {'line': 'string'}, 2, 2, id="line_string"),
        pytest.param(0, 2, {'shift': 'string'}, 2, 2, id="shift_string"),
        pytest.param(0, 2, {'brigade': 'string'}, 2, 2, id="brigade_string"),
        pytest.param(0, 2, {'batch_number': '645646'}, 2, 2, id="batch_number_645646"),
        pytest.param(0, 2, {'batch_date': '2024-04-11'}, 1, 0,
                     id="batch_date_2024-04-11"),
        pytest.param(0, 2, {'nomenclature': 'string'}, 2, 2, id="nomenclature_string"),
    ],
)
@pytest.mark.usefixtures("generate_many_task")
@pytest.mark.anyio
async def test_task_get_by_filter(
        task_command_use, page, size, filter_data, result_len, total
) -> None:
    filter_task = FilterData(page=page, size=size, filter=filter_data)
    result = await task_command_use.filter(filter_task)
    assert result.total == total
    assert len(result.data) == result_len


@pytest.mark.parametrize(
    "task_id, update_dict",
    [
        pytest.param("013132f6-cc00-40b0-b1a9-c31c7eb54aa4", {}, id="no_update"),
        pytest.param("013132f6-cc00-40b0-b1a9-c31c7eb54aa4",
                     {'status_closed': True, 'shift': '11111', 'line': '11111',
                      'brigade': '11111',
                      'nomenclature': '11111', 'code_ekn': '11111'}, id="update_many"),
        pytest.param("013132f6-cc00-40b0-b1a9-c31c7eb54aa4", {'batch_number': 23523524},
                     id="update_batch_number"),
        pytest.param("013132f6-cc00-40b0-b1a9-c31c7eb54aa4", {'shift': '11111'},
                     id="update_shift"),
    ],
)
@pytest.mark.anyio
async def test_task_update(
        task_query_use, task_command_use, task, task_id, update_dict
) -> None:
    expected_result = task.model_copy(update=update_dict).model_dump(
        exclude='closed_at')
    update = TaskUpdate(task_id=task_id, update_dict=update_dict)
    result = await task_command_use.update(update)
    assert result.model_dump(exclude='closed_at') == expected_result
    changed_task = await task_query_use.get_by_id(task.id)
    assert changed_task.model_dump(exclude='closed_at') == expected_result


@pytest.mark.parametrize(
    "new_tasks",
    [
        pytest.param([
            {
                "status_closed": True,
                "shift_task_representation": "string",
                "line": "11111",
                "shift": "string",
                "brigade": "string",
                "batch_number": 645646,
                "batch_date": "2024-04-11",
                "nomenclature": "string",
                "code_ekn": "string",
                "identifier_rc": "string",
                "shift_start_time": "2024-04-23T07:19:32.416Z",
                "shift_end_time": "2024-04-23T07:19:32.416Z"
            },
        ], id="update_task"),
        pytest.param([
            {
                "status_closed": True,
                "shift_task_representation": "string",
                "line": "string",
                "shift": "string",
                "brigade": "string",
                "batch_number": 645646,
                "batch_date": "2024-04-11",
                "nomenclature": "string",
                "code_ekn": "string",
                "identifier_rc": "string",
                "shift_start_time": "2024-04-23T07:19:32.416Z",
                "shift_end_time": "2024-04-23T07:19:32.416Z"
            },
        ], id="add_task"),
        pytest.param([
            {
                "status_closed": True,
                "shift_task_representation": "string",
                "line": "string",
                "shift": "string",
                "brigade": "string",
                "batch_number": 4253453,
                "batch_date": "2024-04-11",
                "nomenclature": "string",
                "code_ekn": "string",
                "identifier_rc": "string",
                "shift_start_time": "2024-04-23T07:19:32.416Z",
                "shift_end_time": "2024-04-23T07:19:32.416Z"
            },
            {
                "status_closed": True,
                "shift_task_representation": "string",
                "line": "string",
                "shift": "string",
                "brigade": "string",
                "batch_number": 54765474,
                "batch_date": "2024-04-11",
                "nomenclature": "string",
                "code_ekn": "string",
                "identifier_rc": "string",
                "shift_start_time": "2024-04-23T07:19:32.416Z",
                "shift_end_time": "2024-04-23T07:19:32.416Z"
            },
        ], id="add_2_task"),
        pytest.param([
            {
                "status_closed": True,
                "shift_task_representation": "string",
                "line": "string",
                "shift": "string",
                "brigade": "string",
                "batch_number": 645646,
                "batch_date": "2024-04-11",
                "nomenclature": "string",
                "code_ekn": "string",
                "identifier_rc": "string",
                "shift_start_time": "2024-04-23T07:19:32.416Z",
                "shift_end_time": "2024-04-23T07:19:32.416Z"
            },
            {
                "status_closed": True,
                "shift_task_representation": "string",
                "line": "string",
                "shift": "string",
                "brigade": "string",
                "batch_number": 161616,
                "batch_date": "2024-04-11",
                "nomenclature": "string",
                "code_ekn": "string",
                "identifier_rc": "string",
                "shift_start_time": "2024-04-23T07:19:32.416Z",
                "shift_end_time": "2024-04-23T07:19:32.416Z"
            },
        ], id="add_task_and_update_task")
    ],
)
@pytest.mark.anyio
async def test_task_create(task_query_use, task_command_use, task, new_tasks) -> None:
    tasks = [
        FakeAddTask.model_validate(task, from_attributes=True) for task in new_tasks
    ]
    await task_command_use.add(tasks)
    for add_task in tasks:
        changed_task = await task_query_use.get_by_num_date(add_task.batch_number,
                                                            add_task.batch_date)
        expected_result = add_task.model_dump()
        data_memory = changed_task.model_dump(
            exclude={'id', 'cubes', 'products', 'closed_at'})
        assert data_memory == expected_result
