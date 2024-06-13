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
from aggregate.application.use_case.cubes.command import CubeCommandUseCase
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
    prefix="/cubes",
    tags=["Cubes"],
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
    cube_command: CubeCommandUseCase = Depends(Provide[AppContainer.cube_command]),
) -> None:
    try:
        logger.info("Создание куба")
        products: list[AddItem] = [
            AddItem.model_validate(product, from_attributes=True)
            for product in new_products
        ]
        await cube_command.add(products)
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
    cube_command: CubeCommandUseCase = Depends(Provide[AppContainer.cube_command]),
) -> AggregationOut:
    try:
        logger.info("Аггрегация куба по id")
        fields_aggr_id: AggregateIdItem = AggregateIdItem.model_validate(
            aggregation, from_attributes=True
        )
        item: ItemResponse = await cube_command.aggregate(fields_aggr_id)
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
    cube_command: CubeCommandUseCase = Depends(Provide[AppContainer.cube_command]),
) -> AggregationOut:
    try:
        logger.info("Аггрегация куба по дате и номеру")
        fields_aggr_data_num: AggregateDataNumberItem = (
            AggregateDataNumberItem.model_validate(aggregation, from_attributes=True)
        )
        item: ItemResponse = await cube_command.aggregate(fields_aggr_data_num)
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
    cube_command: CubeCommandUseCase = Depends(Provide[AppContainer.cube_command]),
) -> AggregationOut:
    try:
        logger.info("Деаггрегация куба по id")
        fields_deaggr_id: AggregateIdItem = AggregateIdItem.model_validate(
            aggregation, from_attributes=True
        )
        item: ItemResponse = await cube_command.deaggregate(fields_deaggr_id)
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
    cube_command: CubeCommandUseCase = Depends(Provide[AppContainer.cube_command]),
) -> AggregationOut:
    try:
        logger.info("Деаггрегация куба по дате и номеру")
        fields_deaggr_data_num: AggregateDataNumberItem = (
            AggregateDataNumberItem.model_validate(aggregation, from_attributes=True)
        )
        item: ItemResponse = await cube_command.deaggregate(fields_deaggr_data_num)
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
    cube_command: CubeCommandUseCase = Depends(Provide[AppContainer.cube_command]),
) -> ItemDetail:
    try:
        logger.info("Поиск куба по id")
        fields_deaggr_id: SearchIdItem = SearchIdItem.model_validate(
            search, from_attributes=True
        )
        item: ItemResponse = await cube_command.search(fields_deaggr_id)
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
    cube_command: CubeCommandUseCase = Depends(Provide[AppContainer.cube_command]),
) -> ItemDetail:
    try:
        logger.info("Поиск куба по дате и номеру")
        fields_deaggr_data_num: SearchDataNumberItem = (
            SearchDataNumberItem.model_validate(search, from_attributes=True)
        )
        item: ItemResponse = await cube_command.search(fields_deaggr_data_num)
        return ItemDetail.model_validate(item, from_attributes=True)
    except NotFoundException as e:
        raise NotFound(detail=e.detail)
    except SQLAlchemyError:
        raise SQLError()
