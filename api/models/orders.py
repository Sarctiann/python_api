__all__ = ["Order", "StoredOrder"]

from pydantic import BaseModel, Field
from pydantic_mongo import PydanticObjectId
from enum import Enum


class OrderStatus(Enum):
    shopping = "shopping"
    completed = "completed"
    cancelled = "cancelled"


class OrderProduct(BaseModel):
    product_id: PydanticObjectId
    price: float
    quantity: int


class Order(BaseModel):
    customer_id: PydanticObjectId
    status: OrderStatus = OrderStatus.shopping
    order_products: list[OrderProduct]


class StoredOrder(Order):
    id: PydanticObjectId = Field(alias="_id")
