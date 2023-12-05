from datetime import datetime

from pydantic import BaseModel


class ReviewModel(BaseModel):
    id: int
    product_id: int
    customer_id: str
    rating: int
    title: str
    comment: str
    created_at: datetime
    updated_at: datetime


class ReviewCreate(BaseModel):
    title: str
    rating: int
    comment: str
