from pydantic import BaseModel
from typing import Optional

class PriceRange(BaseModel):
    min: float
    max: float

class ProductFilters(BaseModel):
    category: list[int] = []
    style: list[int] = []
    material: list[int] = []
    color: list[int] = []
    dimentions: list[int] = []
    price: PriceRange = None
    short_based_on_ratings: bool = False
    number_of_products_to_fetch: int = None
    location: int = None