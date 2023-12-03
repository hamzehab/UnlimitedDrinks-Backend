from datetime import datetime

from pydantic import BaseModel


class OrderItemModel(BaseModel):
    id: int
    category: str
    name: str
    image: str
    brand: str
    price: float
    quantity: int
    subtotal: float


class OrderModel(BaseModel):
    id: int
    orderItems: list[OrderItemModel]
    subtotal: float
    status: int
    full_name: str
    shipAddress: str
    shippedDate: datetime | None = None
    orderDate: str


class CheckoutModel(BaseModel):
    address_id: int
    cartItems: list[dict]
