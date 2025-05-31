from fastapi import APIRouter, Response

from utils.schemas import commonResponse
from .crud import get_about_details

about_router = APIRouter()

@about_router.get('/', summary="get about", response_model=commonResponse)
def get_about(response: Response):
    return get_about_details(response)