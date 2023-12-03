from api.address import api as address
from api.category import api as category
from api.customer import api as customer
from api.orders import api as orders
from api.product import api as products
from fastapi import APIRouter

router = APIRouter()

router.include_router(orders.router, tags=["order"], prefix="/order")
router.include_router(category.router, tags=["category"], prefix="/category")
router.include_router(products.router, tags=["product"], prefix="/product")
router.include_router(customer.router, tags=["customer"], prefix="/customer")
router.include_router(address.router, tags=["address"], prefix="/address")
