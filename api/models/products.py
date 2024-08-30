__all__ = ["Product", "StoredProduct", "UpdationProduct"]

from pydantic import BaseModel, Field
from pydantic_mongo import PydanticObjectId
from datetime import datetime


class Product(BaseModel):
    seller_id: PydanticObjectId
    name: str
    price: float
    quantity: int
    description: str
    image: str
    deactivated_at: datetime | None = Field(default=None)


class UpdationProduct(BaseModel):
    seller_id: PydanticObjectId = Field(default=None)
    name: str | None
    price: float | None
    quantity: int | None
    description: str | None
    image: str | None


class StoredProduct(Product):
    id: PydanticObjectId = Field(alias="_id")
