from fastapi import APIRouter

from src.analytics.service import get_sales_by_product_service

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
)


@router.get("/sales-by-product")
def sales_by_product():
    return get_sales_by_product_service()