from pydantic import BaseModel
from utils.schemas import responseParameter
from typing import Sequence


class UserUpdate(BaseModel):
    name: str
    email: str
    mobile: int
    address_house_no: str = ""
    address_landmark: str = ""
    address_city: str = ""
    address_pincode: str = ""
    address_state: str = ""
    address_country: str = ""

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: str
    password: str

    class Config:
        from_attributes = True

class Location(BaseModel):
    country: str
    state: str
    city: str
    pincode: str
    landmark: str