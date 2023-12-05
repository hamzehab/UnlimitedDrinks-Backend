from datetime import datetime

from api.review.models import ReviewModel
from pydantic import BaseModel


class ProductModel(BaseModel):
    id: int
    category_name: str
    image: str
    name: str
    description: str
    brand: str
    price: float
    quantity: int
    reviews: list[ReviewModel]
    rating: float
    created_at: datetime
    updated_at: datetime
