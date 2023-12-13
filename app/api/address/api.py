from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from loguru import logger

from app.db.schema import Address, Customer

from .models import AddressCreate, AddressModel, SingleAddressModel

router = APIRouter()


async def does_customer_exist(customer_id: str):
    try:
        customer = await Customer.get(id=customer_id)
        if customer:
            return True
        else:
            return False
    except Exception:
        return False


@router.get("/{customer_id}", tags=["address"])
async def get_customer_addresses(customer_id: str):
    customerExists = await does_customer_exist(customer_id)
    if not customerExists:
        logger.error("Customer does not exist")
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
        logger.error(str(e))
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
            logger.error(str(e))
            raise HTTPException(status_code=404, detail=str(e))
    else:
        logger.error("Customer not Found")
        raise HTTPException(status_code=404, detail="Customer not Found")


@router.post("/updateMain/{customer_id}/{address_id}", tags=["address"])
async def change_main_address(customer_id: str, address_id: int):
    exists = await does_customer_exist(customer_id)
    if exists:
        try:
            addresses = await Address.filter(customer_id=customer_id)
            for address in addresses:
                address.is_default = False
                await address.save()
            await Address.get(id=address_id).update(is_default=True)
            return SingleAddressModel(**dict(address))
        except Exception as e:
            logger.error(str(e))
            raise HTTPException(status_code=404, detail=str(e))

    else:
        logger.error("Customer not Found")
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
            logger.error(str(e))
            raise HTTPException(status_code=404, detail=str(e))
    else:
        logger.error("Customer not found")
        raise HTTPException(status_code=404, detail="Customer not Found")


@router.delete("/delete/{customer_id}/{address_id}")
async def delete_selected_address(customer_id: str, address_id: int):
    try:
        address = await Address.filter(id=address_id, customer_id=customer_id)
        if address[0]:
            await address[0].delete()
            return True
        else:
            return False
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/isMain/{customer_id}/{address_id}")
async def check_if_address_main(customer_id: str, address_id: int):
    try:
        address = await Address.get(id=address_id, customer_id=customer_id)
        if address.is_default:
            return True
        else:
            return False
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=404, detail=str(e))
