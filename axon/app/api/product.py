from typing import List

from app.schemas.aggregate import Aggregation
from app.schemas.products import Product
from app.services.products import ProductRepository
from app.utils.exception import (BatchClosed, BatchNone, ErrorCodeAttached,
                                 ErrorCodeUsed, ProductNotExist)
from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


@router.post("/add", status_code=status.HTTP_201_CREATED)
async def add_product(new_products: List[Product]):
    try:
        await ProductRepository().add_product(new_products)
    except SQLAlchemyError:
        raise SQLAlchemyError(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Bad request (add product)'
        )


@router.patch(
    "/aggregate", status_code=status.HTTP_201_CREATED, response_model=dict
)
async def aggregate_product(aggregation: Aggregation):
    try:
        return await ProductRepository().aggregate_product(aggregation)
    except ProductNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product does not exist",
        )
    except ErrorCodeAttached:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unique code is attached to another batch"
        )
    except ErrorCodeUsed as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Unique code already used at {error.data}'
        )
    except BatchNone:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Batch is None",
        )
    except BatchClosed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Batch is closed",
        )
    except SQLAlchemyError:
        raise SQLAlchemyError(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Bad request (aggregate product)'
        )
