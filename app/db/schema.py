from enum import IntEnum

from tortoise import fields
from tortoise.models import Model


class Customer(Model):
    id = fields.CharField(pk=True, max_length=255, unique=True)
    first_name = fields.CharField(max_length=255)
    last_name = fields.CharField(max_length=255)
    email = fields.CharField(max_length=255, unique=True)
    addresses: fields.ReverseRelation["Address"]
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "customers"
        table_description = "The 'customers' table stores information about customers."


class Category(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    description = fields.TextField()
    products: fields.ReverseRelation["Product"]
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "categories"
        table_description = "The 'categories' table classifies products into distinct categories, aiding in data organization and retrieval."


class Product(Model):
    id = fields.IntField(pk=True)
    category = fields.ForeignKeyField("models.Category", related_name="products")
    image = fields.CharField(max_length=255)
    name = fields.CharField(max_length=255)
    description = fields.TextField()
    brand = fields.CharField(max_length=255)
    price = fields.DecimalField(max_digits=10, decimal_places=2)
    quantity = fields.IntField()
    reviews: fields.ReverseRelation["Review"]
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "products"
        table_description = "The 'products' table stores information about products."


class Address(Model):
    id = fields.IntField(pk=True)
    customer = fields.ForeignKeyField("models.Customer", related_name="addresses")
    first_name = fields.CharField(max_length=255)
    last_name = fields.CharField(max_length=255)
    street = fields.CharField(max_length=255)
    street2 = fields.CharField(max_length=255, null=True)
    city = fields.CharField(max_length=255)
    state = fields.CharField(max_length=2)
    zip_code = fields.CharField(max_length=5)
    country = fields.CharField(max_length=3, default="USA")
    is_default = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    def full_street(self):
        return (
            f"{self.street} {self.street2}, {self.city} {self.state} {self.zip_code}"
            if self.street2
            else f"{self.street}, {self.city} {self.state} {self.zip_code}"
        )

    class Meta:
        table = "addresses"
        table_description = (
            "The 'addresses' table stores addresses associated with customers."
        )


class RatingEnum(IntEnum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5


class Review(Model):
    id = fields.IntField(pk=True)
    product = fields.ForeignKeyField("models.Product", related_name="reviews")
    customer = fields.ForeignKeyField("models.Customer", related_name="reviews")
    rating = fields.IntEnumField(RatingEnum)
    title = fields.CharField(max_length=255)
    comment = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "reviews"
        table_description = (
            "The 'reviews' table stores reviews associated with products."
        )


class StatusType(IntEnum):
    PROCESSING = 0
    SHIPPED = 1
    DELIVERED = 2


class Order(Model):
    id = fields.IntField(pk=True)
    customer = fields.ForeignKeyField("models.Customer", related_name="orders")
    total_price = fields.DecimalField(max_digits=10, decimal_places=2)
    shipAddress = fields.ForeignKeyField("models.Address", related_name="orders")
    shippedDate = fields.DateField(null=True)
    status: StatusType = fields.IntEnumField(StatusType)
    orderDate = fields.DatetimeField(auto_now_add=True)


class OrderItem(Model):
    id = fields.IntField(pk=True)
    order = fields.ForeignKeyField("models.Order", related_name="orderItems")
    product = fields.ForeignKeyField("models.Product", related_name="orderItems")
    quantity = fields.IntField()
    price = fields.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        table = "orderItems"
        table_description = "The 'orderItems' table stores information about each order and which items are within each separate order for each customer. "
