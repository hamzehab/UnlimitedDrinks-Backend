from datetime import datetime

from pydantic import BaseModel


class ReviewModel(BaseModel):
    id: int
    product_id: int
    customer_id: str
    rating: int
    comment: str
    created_at: datetime
    updated_at: datetime


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
