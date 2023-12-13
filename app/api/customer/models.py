from datetime import datetime

from pydantic import BaseModel

from app.api.address.models import AddressModel


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
