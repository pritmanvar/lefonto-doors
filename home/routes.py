from fastapi import APIRouter, Response

from utils.schemas import commonResponse
from .crud import get_home_details
home_router = APIRouter()

@home_router.get('/', summary="get home", response_model=commonResponse)
def get_home(response: Response):
    return get_home_details(response)