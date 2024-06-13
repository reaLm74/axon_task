import logging

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status
from shared_kernel.infra.container import AppContainer
from sqlalchemy.exc import SQLAlchemyError

from aggregate.application.dto import (
    AddItem,
    AggregateDataNumberItem,
    AggregateIdItem,
    ItemResponse,
    SearchDataNumberItem,
    SearchIdItem,
)
from aggregate.application.use_case.products import ProductCommandUseCase
from aggregate.domain.exceptions import BadRequestException, NotFoundException
from aggregate.presentation.dto import (
    AggregationDataNumber,
    AggregationId,
    AggregationOut,
    ItemDetail,
    ItemIn,
    SearchDataNumber,
    SearchId,
)
from aggregate.presentation.exceptions import (
    BadRequest,
    Message,
    NotFound,
    SQLError,
)

logger = logging.getLogger("api")
router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


@router.post(
    path="/add",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": Message},
    },
)
@inject
async def add(
    new_products: list[ItemIn],
    product_command: ProductCommandUseCase = Depends(
        Provide[AppContainer.product_command]
    ),
) -> None:
    try:
        logger.info("Создание продукта")
        products: list[AddItem] = [
            AddItem.model_validate(product, from_attributes=True)
            for product in new_products
        ]
        await product_command.add(products)
    except SQLAlchemyError:
        raise SQLError()


@router.patch(
    path="/aggregate/by_batch_id",
    status_code=status.HTTP_201_CREATED,
    response_model=AggregationOut,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": Message},
        status.HTTP_400_BAD_REQUEST: {"model": Message},
    },
)
@inject
async def aggregate_id(
    aggregation: AggregationId,
    product_command: ProductCommandUseCase = Depends(
        Provide[AppContainer.product_command]
    ),
) -> AggregationOut:
    try:
        logger.info("Аггрегация продукта по id")
        fields_aggr_id: AggregateIdItem = AggregateIdItem.model_validate(
            aggregation, from_attributes=True
        )
        item: ItemResponse = await product_command.aggregate(fields_aggr_id)
        return AggregationOut.model_validate(item, from_attributes=True)
    except NotFoundException as e:
        raise NotFound(detail=e.detail)
    except BadRequestException as e:
        raise BadRequest(detail=e.detail)
    except SQLAlchemyError:
        raise SQLError()


@router.patch(
    path="/aggregate/by_batch_datenumber",
    status_code=status.HTTP_201_CREATED,
    response_model=AggregationOut,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": Message},
        status.HTTP_400_BAD_REQUEST: {"model": Message},
    },
)
@inject
async def aggregate_data_num(
    aggregation: AggregationDataNumber,
    product_command: ProductCommandUseCase = Depends(
        Provide[AppContainer.product_command]
    ),
) -> AggregationOut:
    try:
        logger.info("Аггрегация продукта по дате и номеру")
        fields_aggr_data_num: AggregateDataNumberItem = (
            AggregateDataNumberItem.model_validate(aggregation, from_attributes=True)
        )
        item: ItemResponse = await product_command.aggregate(fields_aggr_data_num)
        return AggregationOut.model_validate(item, from_attributes=True)
    except NotFoundException as e:
        raise NotFound(detail=e.detail)
    except BadRequestException as e:
        raise BadRequest(detail=e.detail)
    except SQLAlchemyError:
        raise SQLError()


@router.patch(
    path="/deaggregate/by_batch_id",
    status_code=status.HTTP_201_CREATED,
    response_model=AggregationOut,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": Message},
        status.HTTP_400_BAD_REQUEST: {"model": Message},
    },
)
@inject
async def deaggregate_id(
    aggregation: AggregationId,
    product_command: ProductCommandUseCase = Depends(
        Provide[AppContainer.product_command]
    ),
) -> AggregationOut:
    try:
        logger.info("Деаггрегация продукта по id")
        fields_deaggr_id: AggregateIdItem = AggregateIdItem.model_validate(
            aggregation, from_attributes=True
        )
        item: ItemResponse = await product_command.deaggregate(fields_deaggr_id)
        return AggregationOut.model_validate(item, from_attributes=True)
    except NotFoundException as e:
        raise NotFound(detail=e.detail)
    except BadRequestException as e:
        raise BadRequest(detail=e.detail)
    except SQLAlchemyError:
        raise SQLError()


@router.patch(
    path="/deaggregate/by_batch_datenumber",
    status_code=status.HTTP_201_CREATED,
    response_model=AggregationOut,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": Message},
        status.HTTP_400_BAD_REQUEST: {"model": Message},
    },
)
@inject
async def deaggregate_data_num(
    aggregation: AggregationDataNumber,
    product_command: ProductCommandUseCase = Depends(
        Provide[AppContainer.product_command]
    ),
) -> AggregationOut:
    try:
        logger.info("Деаггрегация продукта по дате и номеру")
        fields_deaggr_data_num: AggregateDataNumberItem = (
            AggregateDataNumberItem.model_validate(aggregation, from_attributes=True)
        )
        item: ItemResponse = await product_command.deaggregate(fields_deaggr_data_num)
        return AggregationOut.model_validate(item, from_attributes=True)
    except NotFoundException as e:
        raise NotFound(detail=e.detail)
    except BadRequestException as e:
        raise BadRequest(detail=e.detail)
    except SQLAlchemyError:
        raise SQLError()


@router.patch(
    path="/search/by_batch_id",
    status_code=status.HTTP_200_OK,
    response_model=ItemDetail,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": Message},
        status.HTTP_400_BAD_REQUEST: {"model": Message},
    },
)
@inject
async def search_id(
    search: SearchId,
    product_command: ProductCommandUseCase = Depends(
        Provide[AppContainer.product_command]
    ),
) -> ItemDetail:
    try:
        logger.info("Поиск продукта по id")
        fields_deaggr_id: SearchIdItem = SearchIdItem.model_validate(
            search, from_attributes=True
        )
        item: ItemResponse = await product_command.search(fields_deaggr_id)
        return ItemDetail.model_validate(item, from_attributes=True)
    except NotFoundException as e:
        raise NotFound(detail=e.detail)
    except SQLAlchemyError:
        raise SQLError()


@router.patch(
    path="/search/by_batch_datenumber",
    status_code=status.HTTP_200_OK,
    response_model=ItemDetail,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": Message},
        status.HTTP_400_BAD_REQUEST: {"model": Message},
    },
)
@inject
async def search_data_num(
    search: SearchDataNumber,
    product_command: ProductCommandUseCase = Depends(
        Provide[AppContainer.product_command]
    ),
) -> ItemDetail:
    try:
        logger.info("Поиск продукта по дате и номеру")
        fields_deaggr_data_num: SearchDataNumberItem = (
            SearchDataNumberItem.model_validate(search, from_attributes=True)
        )
        item: ItemResponse = await product_command.search(fields_deaggr_data_num)
        return ItemDetail.model_validate(item, from_attributes=True)
    except NotFoundException as e:
        raise NotFound(detail=e.detail)
    except SQLAlchemyError:
        raise SQLError()
