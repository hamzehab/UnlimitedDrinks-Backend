from pydantic import BaseModel


class AddressCreate(BaseModel):
    first_name: str
    last_name: str
    street: str
    street2: str | None = None
    city: str
    state: str
    zip_code: str


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
