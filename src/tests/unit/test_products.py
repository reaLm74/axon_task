import pytest
from aggregate.application.dto.items import (
    AddItem,
    AggregateDataNumberItem,
    SearchDataNumberItem,
    SearchIdItem,
)


@pytest.mark.parametrize(
    "batch_date, batch_number, product_code",
    [pytest.param("2024-04-11", 645646, "product", id="add_products")],
)
@pytest.mark.anyio
async def test_products_add(
        product_command_use, task, product, batch_date, batch_number, product_code
) -> None:
    list_cubes = [AddItem(
        batch_date=batch_date, batch_number=batch_number, product_code=product_code
    )]
    await product_command_use.add(list_cubes)
    search_item = SearchDataNumberItem(
        batch_date=batch_date, batch_number=batch_number, product_code=product_code
    )
    changed_task = await product_command_use.search(search_item)
    for item in list_cubes:
        expected_result = item.model_dump(exclude={'batch_date', 'batch_number'})
        data_memory = changed_task.model_dump(
            exclude={'is_aggregated', 'aggregated_at', 'id', 'task_id'})
        assert data_memory == expected_result


@pytest.mark.anyio
async def test_products_search(product_command_use, task, product) -> None:
    expected_result = product.model_dump()
    search_item = SearchDataNumberItem(
        batch_date=task.batch_date,
        batch_number=task.batch_number,
        product_code=product.product_code
    )
    result_search = await product_command_use.search(search_item)
    data_memory = result_search.model_dump()
    assert data_memory == expected_result
    search_item = SearchIdItem(
        task_id=task.id,
        product_code=product.product_code
    )
    result_search = await product_command_use.search(search_item)
    data_memory = result_search.model_dump()
    assert data_memory == expected_result


@pytest.mark.anyio
async def test_products_aggregate_deaggregate(
        product_command_use, task, product
) -> None:
    expected_result = product.model_copy().model_dump()
    search_item = AggregateDataNumberItem(
        batch_date=task.batch_date,
        batch_number=task.batch_number,
        product_code=product.product_code
    )
    result_search = await product_command_use.aggregate(search_item)
    data_memory = result_search.model_dump()
    assert data_memory["is_aggregated"] != expected_result['is_aggregated']
    assert data_memory["aggregated_at"] != expected_result["aggregated_at"]
    result_search = await product_command_use.deaggregate(search_item)
    data_memory = result_search.model_dump()
    assert data_memory["is_aggregated"] == expected_result['is_aggregated']
    assert data_memory["aggregated_at"] == expected_result["aggregated_at"]
    search_item = SearchIdItem(
        task_id=task.id,
        product_code=product.product_code
    )
    result_search = await product_command_use.aggregate(search_item)
    data_memory = result_search.model_dump()
    assert data_memory["is_aggregated"] != expected_result['is_aggregated']
    assert data_memory["aggregated_at"] != expected_result["aggregated_at"]
    result_search = await product_command_use.deaggregate(search_item)
    data_memory = result_search.model_dump()
    assert data_memory["is_aggregated"] == expected_result['is_aggregated']
    assert data_memory["aggregated_at"] == expected_result["aggregated_at"]
