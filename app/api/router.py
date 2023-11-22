from api import api as api
from fastapi import APIRouter

router = APIRouter()

router.include_router(api.router)
