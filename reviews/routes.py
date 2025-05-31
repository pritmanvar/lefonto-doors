from fastapi import APIRouter, Depends, Response

from utils.schemas import commonResponse
from utils.utils import get_token
from .schemas import Review
from .crud import add_review_details

reviews_router = APIRouter()

@reviews_router.post('/', summary="add review", response_model=commonResponse)
def add_review(response: Response, data: Review, user_details: dict = Depends(get_token)):
    return add_review_details(response, data, user_details['email'])