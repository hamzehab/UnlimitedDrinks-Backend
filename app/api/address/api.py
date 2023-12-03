from api.customer.api import does_customer_exist
from db.schema import Address, Customer
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from .models import AddressCreate, AddressModel, SingleAddressModel

router = APIRouter()


@router.get("/{customer_id}", tags=["address"])
async def get_customer_addresses(customer_id: str):
    customerExists = await does_customer_exist(customer_id)
    if not customerExists:
        raise HTTPException(status_code=404, detail="Customer does not exist")

    try:
        customer = await Customer.get(id=customer_id)
        addresses = await customer.addresses.all()
        other_addresses = []
        for address in addresses:
            if address.is_default:
                main_address = SingleAddressModel(**dict(address))
            else:
                other_addresses.append(SingleAddressModel(**dict(address)))
        return AddressModel(main_address=main_address, addresses=other_addresses)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/add/{customer_id}", tags=["address"])
async def add_customer_address(customer_id: str, address: AddressCreate):
    exists = await does_customer_exist(customer_id)
    if exists:
        try:
            new_address = await Address.create(
                **address.model_dump(), customer_id=customer_id
            )
            return SingleAddressModel(**dict(new_address))
        except Exception as e:
            raise HTTPException(status_code=404, detail=str(e))
    else:
        raise HTTPException(status_code=404, detail="Customer not Found")


@router.post("/updateMain/{customer_id}/{address_id}", tags=["address"])
async def change_main_address(customer_id: str, address_id: int):
    exists = await does_customer_exist(customer_id)
    if exists:
        addresses = await Address.filter(customer_id=customer_id)
        for address in addresses:
            address.is_default = False
            await address.save()
        await Address.get(id=address_id).update(is_default=True)
        return SingleAddressModel(**dict(address))

    else:
        raise HTTPException(status_code=404, detail="Customer not Found")


@router.post("/update/{customer_id}/{address_id}", tags=["address"])
async def update_address(customer_id: str, address_id: int, address: AddressCreate):
    exists = await does_customer_exist(customer_id)
    if exists:
        try:
            address_to_update = await Address.get(id=address_id)

            if (AddressCreate(**dict(address_to_update))).model_dump(
                exclude_unset=True, exclude_none=True
            ) == address.model_dump(exclude_unset=True, exclude_none=True):
                return JSONResponse(
                    status_code=status.HTTP_204_NO_CONTENT,
                    content={"detail": "No changes were made"},
                )

            fields_to_update = [
                "first_name",
                "last_name",
                "street",
                "street2",
                "city",
                "state",
                "zip_code",
            ]
            for field in fields_to_update:
                if getattr(address_to_update, field) != getattr(address, field):
                    setattr(address_to_update, field, getattr(address, field))

            await address_to_update.save()
            updated_address = await Address.get(id=address_id)
            return SingleAddressModel(**dict(updated_address))
        except Exception as e:
            raise HTTPException(status_code=404, detail=str(e))
    else:
        raise HTTPException(status_code=404, detail="Customer not Found")


@router.delete("/delete/{customer_id}/{address_id}")
async def delete_selected_address():
    pass
