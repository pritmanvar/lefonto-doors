from pydantic import BaseModel

class Review(BaseModel):
    product: int
    rating: float
    review_text: str