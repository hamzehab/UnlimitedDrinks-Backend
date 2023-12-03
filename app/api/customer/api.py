from api.address.models import AddressCreate, AddressModel, SingleAddressModel
from db.schema import Address, Customer
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from loguru import logger

from .models import CustomerCreate, CustomerModel

router = APIRouter()


# Profile Endpoints
@router.get("/exists/{customer_id}", response_model=bool, tags=["customer"])
async def does_customer_exist(customer_id: str):
    try:
        customer = await Customer.get(id=customer_id)
        if customer:
            return True
        else:
            return False
    except Exception:
        return False


@router.get("/{customer_id}", tags=["customer"])
async def get_customer(customer_id: str):
    try:
        customer = await Customer.get(id=customer_id)
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not Found")
    except Exception:
        raise HTTPException(status_code=404, detail="Customer not Found")

    logger.info(f"Retrieved {customer_id}'s profile")
    try:
        addresses = await customer.addresses.all()
        logger.info(f"Retrieved {customer_id}'s addresses")
        other_addresses = []
        for address in addresses:
            if address.is_default:
                main_address = SingleAddressModel(**dict(address))
            else:
                other_addresses.append(SingleAddressModel(**dict(address)))

        return CustomerModel(
            **dict(customer),
            addresses=AddressModel(
                main_address=main_address, addresses=other_addresses
            ),
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/create", response_model=CustomerModel, tags=["customer"])
async def create_customer(customer: CustomerCreate, address: AddressCreate):
    customerExists = await does_customer_exist(customer.id)
    if customerExists:
        raise HTTPException(status_code=404, detail="Customer already exists")
    try:
        customer = await Customer.create(**customer.dict())
        address = await Address.create(
            **address.model_dump(), customer_id=customer.id, is_default=True
        )

        return CustomerModel(
            **dict(customer),
            addresses=AddressModel(
                main_address=SingleAddressModel(**dict(address)), addresses=[]
            ),
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/editName/{customer_id}", tags=["customer"])
async def edit_customer_name(customer_id: str, customer_name: dict):
    customerExists = await does_customer_exist(customer_id)
    if not customerExists:
        raise HTTPException(status_code=404, detail="Customer does not exist")
    try:
        customer = await Customer.get(id=customer_id)
        if (
            customer.first_name == customer_name["first_name"]
            and customer.last_name == customer_name["last_name"]
        ):
            return JSONResponse(
                status_code=status.HTTP_204_NO_CONTENT,
                content={"detail": "No changes were made"},
            )

        if customer.first_name != customer_name["first_name"]:
            customer.first_name = customer_name["first_name"]

        if customer.last_name != customer_name["last_name"]:
            customer.last_name = customer_name["last_name"]

        await customer.save()

        updated_customer = await Customer.get(id=customer_id)
        return {
            "first_name": updated_customer.first_name,
            "last_name": updated_customer.last_name,
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
