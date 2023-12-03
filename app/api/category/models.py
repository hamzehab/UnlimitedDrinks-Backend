from datetime import datetime

from pydantic import BaseModel


class CategoryCreate(BaseModel):
    name: str
    description: str


class CategoryUpdate(BaseModel):
    name: str | None
    description: str | None


class CategoryModel(BaseModel):
    id: int
    name: str
    description: str
    created_at: datetime
    updated_at: datetime
