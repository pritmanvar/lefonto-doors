from pydantic import BaseModel

class PriceRange(BaseModel):
    min: float
    max: float

class ProductFilters(BaseModel):
    category: list[int] = []
    style: list[int] = []
    material: list[int] = []
    color: list[int] = []
    price: PriceRange = None