from src.analytics.queries import (
    get_sales_by_product,
    get_sales_by_customer,
    get_sales_summary,
)


def get_sales_by_product_service():
    return get_sales_by_product()


def get_sales_by_customer_service():
    return get_sales_by_customer()


def get_sales_summary_service():
    return get_sales_summary()