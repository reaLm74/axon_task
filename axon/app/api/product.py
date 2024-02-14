from typing import List

from fastapi import APIRouter, HTTPException
from fastapi import status
from sqlalchemy.exc import SQLAlchemyError

from app.schemas.aggregate import Aggregation
from app.schemas.products import Product
from app.services.products import ProductRepository
from app.utils.exception import (ProductNotExist, ErrorCodeAttached, BatchNone,
                                 ErrorCodeUsed, BatchClosed)

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


@router.post("/add", status_code=status.HTTP_200_OK)
async def add_product(new_products: List[Product]):
    try:
        await ProductRepository().add_product(new_products)
    except SQLAlchemyError as error:
        raise SQLAlchemyError(f'Error in "add_product": {error}')


@router.patch("/aggregate", status_code=status.HTTP_200_OK, response_model=dict)
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
    except SQLAlchemyError as error:
        return SQLAlchemyError(f'Error in "aggregate_product": {error}')
