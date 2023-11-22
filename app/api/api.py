import json
import os
import random

import stripe
from db.schema import Address, Category, Customer, Order, OrderItem, Product
from fastapi import APIRouter, HTTPException, Request
from loguru import logger

from .models import (
    AddressCreate,
    AddressModel,
    CategoryCreate,
    CategoryModel,
    CategoryUpdate,
    CustomerCreate,
    CustomerModel,
    OrderItemModel,
    OrderModel,
    ProductModel,
    ReviewModel,
    SingleAddressModel,
)

router = APIRouter()


# Category Endpoints
@router.get("/category/{category_name}", response_model=bool, tags=["category"])
async def does_category_exist(category_name: str):
    category_name = category_name.lower().replace("-", " ")
    try:
        category = await Category.filter(name=category_name)
        if category:
            return True
        else:
            return False
    except Exception:
        return False


@router.get("/categories", response_model=list[CategoryModel], tags=["category"])
async def get_all_categories():
    try:
        categories = await Category.all().order_by("id")
        logger.info("Retrieved all categories")
        return [CategoryModel(**dict(category)) for category in categories]
    except Exception as e:
        logger.info(str(e))
        raise HTTPException(status_code=404, detail="Something went wrong")


@router.post("/category", response_model=CategoryModel, tags=["category"])
async def create_category(category: CategoryCreate):
    try:
        exists = await does_category_exist(category.name)
        if not exists:
            new_category = await Category.create(
                name=category.name, description=category.description
            )

            logger.info(f"{new_category.name} category created successfully")
            return CategoryModel(**dict(new_category))
        else:
            logger.info(f"Category with that name ({category.name}) already exists")
            raise HTTPException(
                status_code=403, detail=f"Category {category.name} already exists"
            )

    except Exception as e:
        logger.info(str(e))
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/category/{category_id}", tags=["category"])
async def delete_category(category_id: int):
    try:
        await Category.get(id=category_id).delete()
        return {"message": "Category deleted successfully"}
    except Exception as e:
        logger.info(str(e))
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/category/{category_id}", tags=["category"])
async def update_category(category_id: int, category: CategoryUpdate):
    category.name = category.name.lower()
    try:
        categoryFound = await Category.get(id=category_id)
        if not categoryFound:
            return {"message": "Category with that id does not exist"}

        attributesToUpdate = {
            attr: value for attr, value in category if value is not None and value != ""
        }
        await Category.get(id=category_id).update(**attributesToUpdate)
        updated_category = await Category.get(id=category_id)
        await updated_category.save()

        logger.info(f"Category {update_category.name} has been updated")
        return {
            "message": "Category updated successfully",
        }

    except Exception as e:
        logger.info(str(e))
        raise HTTPException(status_code=404, detail=str(e))


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


@router.get("/products", tags=["product"])
async def get_all_products():
    try:
        products = await Product.all().order_by("id")
        logger.info(f"Retrieved {len(products)} products")
        return await get_product_reviews(products)
    except Exception as e:
        logger.info(str(e))
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/products/{category_name}", tags=["product"])
async def get_products_by_category(category_name: str):
    category_name = category_name.lower().replace("-", " ")
    try:
        category = await Category.get(name=category_name)
        products = await category.products.all()

        return await get_product_reviews(products)

    except Exception as e:
        logger.info(str(e))
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/product/{product_id}", tags=["product"])
async def get_product_by_id(product_id: int):
    try:
        product = await Product.get(id=product_id)
        category_name = await get_category_name(product)
        reviews = await product.reviews.all()
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
        logger.info(str(e))
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/roulette", response_model=list[ProductModel], tags=["product"])
async def get_four_random_products():
    try:
        products = await Product.all()
        productList = await get_product_reviews(products)
        random.shuffle(productList)
        return productList[:4]

    except Exception as e:
        logger.info(str(e))
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/search/{query}", tags=["product"])
async def search_for_products(query: str):
    try:
        productsByName = await Product.filter(name__icontains=query)
        productsByBrand = await Product.filter(brand__icontains=query)
        products = set(productsByName + productsByBrand)

        return await get_product_reviews(products)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


# Profile Endpoints
@router.get("/customer/exists/{customer_id}", response_model=bool, tags=["customer"])
async def does_customer_exist(customer_id: str):
    try:
        customer = await Customer.get(id=customer_id)
        if customer:
            return True
        else:
            return False
    except Exception:
        return False


@router.get("/customer/{customer_id}", tags=["customer"])
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


@router.post("/create/customer", response_model=CustomerModel, tags=["customer"])
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


# Address Endpoints
@router.get("/customer/{customer_id}/addresses", tags=["address"])
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


@router.post("/address/add/{customer_id}", tags=["address"])
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


@router.post("/address/updateMain/{customer_id}/{address_id}", tags=["address"])
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


@router.post("/checkout/session")
async def checkout(customer_email: str, cartItems: list[dict]):
    stripe.api_key = os.environ["STRIPE_SECRET_KEY"]

    line_items = []
    for item in cartItems:
        product = await Product.get(id=item["product_id"])
        line_items.append(
            {
                "price_data": {
                    "currency": "usd",
                    "product_data": {"name": product.name},
                    "unit_amount": int(product.price * 100),
                },
                "quantity": item["quantity"],
            }
        )

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="payment",
            line_items=line_items,
            customer_email=customer_email,
            success_url=f"{os.environ['URL']}/success",
            cancel_url=f"{os.environ['URL']}/cart",
            metadata={"cartItems": json.dumps(cartItems), "address_id": "123 Main St"},
        )

        return session
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/webhook")
async def webhook(request: Request):
    event = None
    payload = await request.body()
    sig_header = request.headers["stripe-signature"]

    try:
        payload = payload.decode("utf-8")
        event = stripe.Webhook.construct_event(
            payload, sig_header, os.environ["STRIPE_WEBHOOK_SECRET"]
        )
    except ValueError as e:
        # Invalid payload
        raise e
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        raise e

    # Handle the event
    if event["type"] == "checkout.session.completed":
        customer_email = event.data.object.customer_email
        cartItems = json.loads(event.data.object.metadata["cartItems"])
        customer = await Customer.get(email=customer_email)

        try:
            order = await Order.create(
                customer_id=customer.id,
                total_price=event.data.object.amount_total,
                shipAddress_id=1,
                # shipAddress_id=event.data.object.metadata["address_id"],
                shippedDate=None,
                status=0,
            )

            for item in cartItems:
                logger.info(item)
                product = await Product.get(id=item["product_id"])
                product.quantity -= item["quantity"]
                await product.save()
                await OrderItem.create(
                    order_id=order.id,
                    product_id=product.id,
                    quantity=item["quantity"],
                    price=product.price * item["quantity"],
                )
        except Exception as e:
            raise HTTPException(status_code=404, detail=str(e))

    return {"success": True}


# Order Endpoints
@router.get("/orders/{customer_id}", tags=["order"])
async def get_orders(customer_id: str):
    try:
        customer = await Customer.get(id=customer_id)
        orders = await customer.orders.all()
        response = []
        for order in orders:
            address = await Address.get(id=order.shipAddress_id)
            full_name = f"{address.first_name} {address.last_name}"
            shipAddress = address.full_street()
            order_date = (order.orderDate).strftime("%B %d, %Y")

            order_items = await order.orderItems.all()
            orderItemsModelList = []
            for item in order_items:
                product = await Product.get(id=item.product_id)
                category = await Category.get(id=product.category_id)

                orderItemsModelList.append(
                    OrderItemModel(
                        id=item.id,
                        category=category.name,
                        name=product.name,
                        image=product.image,
                        brand=product.brand,
                        price=product.price,
                        quantity=item.quantity,
                        subtotal=item.price,
                    )
                )

            response.append(
                OrderModel(
                    id=order.id,
                    subtotal=order.total_price,
                    orderDate=order_date,
                    status=order.status,
                    full_name=full_name,
                    shipAddress=shipAddress,
                    orderItems=orderItemsModelList,
                )
            )
        return response
    except Exception as e:
        logger.info(str(e))
        raise HTTPException(status_code=404, detail=str(e))
