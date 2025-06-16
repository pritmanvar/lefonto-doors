from fastapi import APIRouter, Response

from utils.schemas import commonResponse
from utils.utils import CommonResponse
from product.schemas import ProductFilters
from product.crud import get_filtered_products_details, get_product_details, get_filters_details

product_router = APIRouter()

@product_router.post('/filters', summary="get product filters", response_model=commonResponse)
def get_filtered_products(response: Response, filters: ProductFilters):
    print(filters)
    return get_filtered_products_details(response=response, filters=filters)

@product_router.get('/product_filters', summary="get product filters", response_model=commonResponse)
def get_filters(response: Response):
    return get_filters_details(response=response)

@product_router.get('/{product_id}', summary="get product details", response_model=commonResponse)
def get_product_info(response: Response, product_id: int):
    return get_product_details(response=response, product_id=product_id)