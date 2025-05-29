from pydantic import BaseModel

class Inquiry(BaseModel):
    name: str
    mobile: int
    message: str
    product: int
    country: str = ""
    state: str = ""
    city: str = ""
    pincode: str = ""
    landmark: str = ""
    address: str = ""