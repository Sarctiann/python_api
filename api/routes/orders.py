__all__ = ["orders_router"]

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from pydantic_mongo import PydanticObjectId

from ..__common_deps import QueryParams, QueryParamsDependency
from ..models import Order, UpdationProduct
from ..services import (
    OrdersServiceDependency,
    ProductsServiceDependency,
    SecurityDependency,
)

orders_router = APIRouter(prefix="/orders", tags=["Orders"])


@orders_router.get("/get_all")
def get_all_orders(
    orders: OrdersServiceDependency,
    security: SecurityDependency,
    params: QueryParamsDependency,
):
    return orders.get_all(params, security)


@orders_router.get("/{id}")
def get_order_by_id(
    id: PydanticObjectId, security: SecurityDependency, orders: OrdersServiceDependency
):

    return orders.get_one(id, security)


@orders_router.get("/get_completed")
def get_completed_orders(security: SecurityDependency, orders: OrdersServiceDependency):
    return orders.get_all(QueryParams(filter="status=completed"), security)


@orders_router.get("/get_cancelled")
def get_cancelled_orders(security: SecurityDependency, orders: OrdersServiceDependency):
    return orders.get_all(QueryParams(filter="status=cancelled"), security)


@orders_router.get("/get_shopping")
def get_shopping_orders(security: SecurityDependency, orders: OrdersServiceDependency):
    return orders.get_all(QueryParams(filter="status=shopping"), security)


@orders_router.get("/get_by_seller")
def get_orders_by_seller_id(
    security: SecurityDependency, orders: OrdersServiceDependency
):
    return orders.get_all(QueryParams(), security)


@orders_router.get("/get_by_customer/{id}")
def get_orders_by_customer_id(
    id: PydanticObjectId, security: SecurityDependency, orders: OrdersServiceDependency
):
    auth_user_id = security.auth_user_id
    assert (
        auth_user_id == id or security.auth_user_role == "admin"
    ), "User does not have access to this orders"

    params = QueryParams(filter=f"custommer_id={id}")
    return orders.get_all(params, security)


@orders_router.get("/get_by_product/{id}")
def get_orders_by_product_id(
    id: PydanticObjectId, security: SecurityDependency, orders: OrdersServiceDependency
):
    params = QueryParams(filter=f"order_products.$product_id={id}")
    return orders.get_all(params, security)


@orders_router.post(
    "/",
)
def create_order(
    order: Order,
    orders: OrdersServiceDependency,
    products: ProductsServiceDependency,
    security: SecurityDependency,
):
    security.is_customer_or_raise
    for product in order.order_products:
        db_product = products.get_one(product.product_id)

        if db_product.get("quantity", 0) < product.quantity:
            return JSONResponse(
                {"error": "Product is out of stock"},
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
            )
        products.update_one(
            product.product_id,
            UpdationProduct(quantity=db_product["quantity"] - product.quantity),
        )

    result = orders.create_one(order)
    if result:
        return {"result message": f"Order created with id: {result}"}
