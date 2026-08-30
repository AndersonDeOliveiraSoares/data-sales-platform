from fastapi import APIRouter

from src.analytics.service import (
    get_sales_by_product_service,
    get_sales_by_customer_service,
    get_sales_summary_service,
)


router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
)


@router.get("/sales-by-product")
def sales_by_product():
    return get_sales_by_product_service()


@router.get("/sales-by-customer")
def sales_by_customer():
    return get_sales_by_customer_service()

@router.get("/sales-summary")
def sales_summary():
    return get_sales_summary_service()