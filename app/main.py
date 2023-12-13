import json
from random import randint, random

from api.router import router
from db.schema import Category, Product
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from settings import settings
from tortoise import expand_db_url
from tortoise.contrib.fastapi import register_tortoise
from tortoise.exceptions import DoesNotExist

data = {}


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_tortoise(
    app,
    config={
        "connections": {
            "default": expand_db_url(str(settings.POSTGRES_URL), "asyncpg")
        },
        "apps": {
            "models": {
                "models": ["db.schema", "aerich.models"],
                "default_connection": "default",
            }
        },
    },
    generate_schemas=True,
    add_exception_handlers=True,
)


app.include_router(router)


@app.on_event("startup")
async def load_products():
    with open("app/db/data.json", "r") as file:
        data.update(json.load(file))

    for category in data["categories"]:
        try:
            category_exists = await Category.get(name=category["name"])
            logger.info(f"Category {category_exists.name} already exists")

        except DoesNotExist:
            await Category.create(**dict(category))
            logger.info(f"Created category {category['name']}")

    for product in data["products"]:
        try:
            product_exists = await Product.get(name=product["name"])
            logger.info(f"Product {product_exists.name} already exists")

        except DoesNotExist:
            try:
                category = await Category.get(name=product["category_name"])
                logger.info(f"Category {category.name} found")

                logger.info(f"Creating product {product['name']}")
                await Product.create(
                    image=product["image"],
                    name=product["name"],
                    description=product["description"],
                    brand=product["brand"],
                    category_id=category.id,
                    price=round(random() + 1, 2),
                    quantity=randint(70, 150),
                )
                logger.info(f"Created product {product['name']}")
            except DoesNotExist:
                logger.info(f"Category {product['category']} not found")
                logger.info(f"Product {product['name']} not created")
                continue
