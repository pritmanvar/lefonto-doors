from fastapi import APIRouter, Depends, Response

from utils.schemas import commonResponse
from utils.validation import ContactDataValidation
from utils.utils import CommonResponse
from contactus.schemas import Inquiry
from contactus.crud import add_inquiry_details

contactus_router = APIRouter()

@contactus_router.post('/inquiry', summary="add inquiry", response_model=commonResponse)
def add_inquiry(response: Response, data: Inquiry):
    is_valid = ContactDataValidation(data)
    print(is_valid, "is_valid")
    if is_valid is not None:
        return CommonResponse(400, "True", 0, "Unacceptable Parameter Value", Message=is_valid)
    return add_inquiry_details(response=response, data=data)