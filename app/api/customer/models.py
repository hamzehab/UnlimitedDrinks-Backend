from datetime import datetime

from api.address.models import AddressModel
from pydantic import BaseModel


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
