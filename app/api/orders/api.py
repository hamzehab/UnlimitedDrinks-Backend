import json
import os
from datetime import datetime, timedelta, timezone

import stripe
from fastapi import APIRouter, HTTPException, Request
from loguru import logger

from app.db.schema import Address, Category, Customer, Order, OrderItem, Product

from .models import CheckoutModel, OrderItemModel, OrderModel

router = APIRouter()


@router.post("/checkout/session")
async def checkout(customer_email: str, data: CheckoutModel):
    stripe.api_key = os.environ["STRIPE_SECRET_KEY"]
    STRIPE_URL = os.environ["STRIPE_URL"]

    line_items = []
    taxes_and_fees = 0
    for item in data.cartItems:
        product = await Product.get(id=item["product_id"])
        unit_amount = int(product.price * 100)
        taxes_and_fees += unit_amount * item["quantity"]
        line_items.append(
            {
                "price_data": {
                    "currency": "usd",
                    "product_data": {"name": product.name},
                    "unit_amount": unit_amount,
                },
                "quantity": item["quantity"],
            }
        )
        logger.info(f"{item} added to line_items for stripe")
    line_items.append(
        {
            "price_data": {
                "currency": "usd",
                "product_data": {"name": "Taxes and Fees"},
                "unit_amount": round(taxes_and_fees * 0.06625),
            },
            "quantity": 1,
        }
    )
    logger.info(f"{taxes_and_fees} added to line_items for stripe")
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="payment",
            line_items=line_items,
            customer_email=customer_email,
            success_url=f"{STRIPE_URL}/success",
            cancel_url=f"{STRIPE_URL}/cart",
            metadata={
                "cartItems": json.dumps(data.cartItems),
                "address_id": data.address_id,
            },
        )

        return session
    except Exception as e:
        logger.error(str(e), "error 404")
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/webhook")
async def webhook(request: Request):
    event = None
    payload = await request.body()
    logger.info("Payload found")
    sig_header = request.headers["stripe-signature"]

    try:
        payload = payload.decode("utf-8")
        logger.info("Payload decoded")
        event = stripe.Webhook.construct_event(
            payload, sig_header, os.environ["STRIPE_WEBHOOK_SECRET"]
        )
    except ValueError as e:
        # Invalid payload
        logger.error(str(e))
        raise e
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        logger.error(str(e))
        raise e

    # Handle the event
    if event["type"] == "checkout.session.completed":
        logger.info("Checkout session completed")
        customer_email = event.data.object.customer_email
        cartItems = json.loads(event.data.object.metadata["cartItems"])
        customer = await Customer.get(email=customer_email)

        try:
            order = await Order.create(
                customer_id=customer.id,
                total_price=event.data.object.amount_total,
                shipAddress_id=event.data.object.metadata["address_id"],
                shippedDate=None,
                status=0,
            )
            logger.info(
                f"Order created with id {order.id} for customer with email {customer.email}"
            )

            for item in cartItems:
                product = await Product.get(id=item["product_id"])
                logger.info(f"Product with {item['product_id']} found")
                product.quantity -= item["quantity"]
                logger.info("Removed quantity for product")
                await product.save()
                orderItem = await OrderItem.create(
                    order_id=order.id,
                    product_id=product.id,
                    quantity=item["quantity"],
                    price=product.price * item["quantity"],
                )
                logger.info(f"Order item created {orderItem}")
        except Exception as e:
            logger.error(str(e))
            raise HTTPException(status_code=404, detail=str(e))

    return {"success": True}


@router.get("/{customer_id}")
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
                        id=product.id,
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
        logger.error(str(e))
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/recent/{customer_id}")
async def is_recent_order_placed(customer_id: str):
    try:
        orders = await Order.filter(customer_id=customer_id).order_by("-orderDate")
        order = orders[0]
        address = await Address.get(id=order.shipAddress_id)
        recent_time_window = datetime.now(timezone.utc) - orders[0].orderDate

        if recent_time_window < timedelta(minutes=2):
            order_items = await order.orderItems.all()
            orderItemsModelList = []
            for item in order_items:
                product = await Product.get(id=item.product_id)
                category = await Category.get(id=product.category_id)

                orderItemsModelList.append(
                    OrderItemModel(
                        id=product.id,
                        category=category.name,
                        name=product.name,
                        image=product.image,
                        brand=product.brand,
                        price=product.price,
                        quantity=item.quantity,
                        subtotal=item.price,
                    )
                )

            return OrderModel(
                id=order.id,
                subtotal=order.total_price,
                orderDate=(order.orderDate).strftime("%B %d, %Y"),
                status=order.status,
                full_name=f"{address.first_name} {address.last_name}",
                shipAddress=address.full_street(),
                orderItems=orderItemsModelList,
            )
        else:
            return False

    except Exception:
        return False
