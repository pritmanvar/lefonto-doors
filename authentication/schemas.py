from pydantic import BaseModel
from utils.schemas import responseParameter
from typing import Sequence


class UserUpdate(BaseModel):
    name: str
    email: str
    mobile: int

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    mobile: int
    password: str

    class Config:
        from_attributes = True

class Location(BaseModel):
    country: str
    state: str
    city: str
    pincode: str
    landmark: str