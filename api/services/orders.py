__all__ = ["OrdersServiceDependency", "OrdersService"]


from typing import Annotated

from fastapi import Depends, HTTPException, status
from pydantic_mongo import PydanticObjectId

from ..__common_deps import QueryParamsDependency
from ..config import COLLECTIONS, db
from ..models import Order, StoredOrder
from ..services import SecurityDependency


def get_orders_by_seler_id_aggregate_query(
    seller_id: PydanticObjectId, pre_filters: dict | None = {}
):
    return [
        # Only if we have an order id
        {"$match": pre_filters},
        # Fist we need to unwind the order products
        {"$unwind": "$order_products"},
        # Then we need to lookup the products collection
        {
            "$lookup": {
                "from": "products",
                "localField": "order_products.product_id",
                "foreignField": "_id",
                "as": "product",
            }
        },
        # Then we need to unwind the product
        {"$unwind": "$product"},
        # Then we need to filter by the seller
        {
            "$match": {
                "product.seller_id": seller_id,
            }
        },
        # Then we can group de orders again
        {
            "$group": {
                "_id": "$_id",
                "order_products": {"$push": "$order_products"},
                "other_fields": {"$first": "$$ROOT"},
            }
        },
        # Finally we need to restructure the document again
        {
            "$replaceRoot": {
                "newRoot": {
                    "$mergeObjects": [
                        "$other_fields",
                        {"order_products": "$order_products"},
                    ]
                }
            }
        },
    ]


class OrdersService:
    assert (collection_name := "orders") in COLLECTIONS
    collection = db[collection_name]

    @classmethod
    def create_one(cls, order: Order):
        document = cls.collection.insert_one(order.model_dump())
        if document:
            return str(document.inserted_id)
        return None

    @classmethod
    def get_all(cls, params: QueryParamsDependency, security: SecurityDependency):
        filter_query: dict = {}

        if security.is_customer:
            filter_query.update(
                {"customer_id": security.auth_user_id},
            )

        if not security.is_seller:
            return [
                StoredOrder.model_validate(order).model_dump()
                for order in params.query_collection(
                    cls.collection, extra_filter=filter_query
                )
            ]

        if security.is_seller and security.auth_user_id:

            return [
                StoredOrder.model_validate(order).model_dump()
                for order in cls.collection.aggregate(
                    get_orders_by_seler_id_aggregate_query(
                        security.auth_user_id, params.filter_dict
                    )
                )
            ]

    @classmethod
    def get_one(cls, id: PydanticObjectId, security: SecurityDependency):
        filter_criteria: dict = {"_id": id}

        if security.is_customer:
            filter_criteria.update(
                {"customer_id": security.auth_user_id},
            )

        if not security.is_seller:
            if db_order := cls.collection.find_one(filter_criteria):
                return StoredOrder.model_validate(db_order).model_dump()
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
                )

        if security.is_seller and security.auth_user_id:

            aggregate_result = [
                StoredOrder.model_validate(order).model_dump()
                for order in cls.collection.aggregate(
                    get_orders_by_seler_id_aggregate_query(
                        security.auth_user_id, {"_id": id}
                    )
                )
            ]

        if len(aggregate_result) > 0:
            return StoredOrder.model_validate(aggregate_result[0]).model_dump()
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
            )


OrdersServiceDependency = Annotated[OrdersService, Depends()]
