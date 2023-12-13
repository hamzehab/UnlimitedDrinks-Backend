from fastapi import APIRouter

from .address import api as address
from .category import api as category
from .customer import api as customer
from .orders import api as orders
from .product import api as products
from .review import api as reviews

router = APIRouter()

router.include_router(orders.router, tags=["order"], prefix="/order")
router.include_router(category.router, tags=["category"], prefix="/category")
router.include_router(products.router, tags=["product"], prefix="/product")
router.include_router(customer.router, tags=["customer"], prefix="/customer")
router.include_router(address.router, tags=["address"], prefix="/address")
router.include_router(reviews.router, tags=["review"], prefix="/review")
