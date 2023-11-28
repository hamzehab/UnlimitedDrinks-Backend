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


class SingleAddressModel(BaseModel):
    id: int
    first_name: str
    last_name: str
    street: str
    street2: str | None
    city: str
    state: str
    country: str
    zip_code: str


class AddressModel(BaseModel):
    main_address: SingleAddressModel
    addresses: list[SingleAddressModel]


class CustomerModel(BaseModel):
    first_name: str
    last_name: str
    email: str
    addresses: AddressModel
    created_at: datetime
    updated_at: datetime


class CustomerCreate(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: str


class AddressCreate(BaseModel):
    first_name: str
    last_name: str
    street: str
    street2: str | None = None
    city: str
    state: str
    zip_code: str


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
