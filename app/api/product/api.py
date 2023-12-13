import random

from fastapi import APIRouter, HTTPException
from loguru import logger

from app.db.schema import Category, Product

from .models import ProductModel, ReviewModel

router = APIRouter()


# Product Endpoints
async def get_category_name(product: Product):
    category = await product.category
    return category.name


async def get_product_reviews(products: Product):
    response = []
    for product in products:
        category_name = await get_category_name(product)
        reviews = await product.reviews.all()
        if reviews:
            total_rating = sum(review.rating for review in reviews)
            rating = total_rating / len(reviews)
        else:
            rating = 0
        response.append(
            ProductModel(
                **dict(product),
                category_name=category_name,
                reviews=[ReviewModel(**dict(review)) for review in reviews],
                rating=rating,
            )
        )
        logger.info(f"Retrieved product {product.name}")
    return response


@router.get("/all")
async def get_all_products():
    try:
        products = await Product.all().order_by("id")
        logger.info(f"Retrieved {len(products)} products")
        return await get_product_reviews(products)
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/category/{category_name}")
async def get_products_by_category(category_name: str):
    category_name = category_name.lower().replace("-", " ")
    try:
        category = await Category.get(name=category_name)
        products = await category.products.all()

        return await get_product_reviews(products)

    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{product_id}")
async def get_product_by_id(product_id: int):
    try:
        product = await Product.get(id=product_id)
        category_name = await get_category_name(product)
        reviews = await product.reviews.all()
        random.shuffle(reviews)

        if reviews:
            total_rating = sum(review.rating for review in reviews)
            rating = total_rating / len(reviews)
        else:
            rating = 0

        return ProductModel(
            **dict(product),
            category_name=category_name,
            reviews=[ReviewModel(**dict(review)) for review in reviews],
            rating=rating,
        )
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/cart/{product_id}")
async def can_add_to_cart(product_id: int, quantity: int):
    try:
        product = await Product.get(id=product_id)
        if quantity <= product.quantity:
            return {"can_add": True}
        else:
            return {"can_add": False, "quantity": product.quantity}
    except Exception as e:
        logger.info(str(e))
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/search/{query}")
async def search_for_products(query: str):
    try:
        productsByName = await Product.filter(name__icontains=query)
        productsByBrand = await Product.filter(brand__icontains=query)
        products = set(productsByName + productsByBrand)

        return await get_product_reviews(products)
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/random/roulette", response_model=list[ProductModel])
async def get_four_random_products():
    try:
        products = await Product.all()
        productList = await get_product_reviews(products)
        random.shuffle(productList)
        return productList[:4]

    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=404, detail=str(e))
