from typing import List

from fastapi import APIRouter
from fastapi import status


from app.schemas.aggregate import Aggregation
from app.schemas.products import Product
from app.services import products


router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


@router.post("/add", status_code=status.HTTP_200_OK)
async def add_product(new_products: List[Product]):
    await products.add_product(new_products)


@router.patch("/aggregate", status_code=status.HTTP_200_OK, response_model=dict)
async def aggregate_product(aggregation: Aggregation):
    return await products.aggregate_product(aggregation)
