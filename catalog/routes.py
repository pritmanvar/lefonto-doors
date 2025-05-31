from fastapi import APIRouter, Response

from utils.schemas import commonResponse
from catalog.crud import get_catalog_details

catalog_router = APIRouter()

@catalog_router.get('/', summary="get catalog", response_model=commonResponse)
def get_catalog(response: Response):
    return get_catalog_details(response)