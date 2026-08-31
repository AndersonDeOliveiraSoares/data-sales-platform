from src.analytics.queries import (
    get_sales_by_product,
    get_sales_by_customer,
    get_sales_summary,
    get_sales_by_month,
    get_available_years,
)


def get_sales_summary_service(
    ano: int | None = None,
    mes: int | None = None,
):
    return get_sales_summary(
        ano=ano,
        mes=mes,
    )


def get_sales_by_product_service(
    ano: int | None = None,
    mes: int | None = None,
):
    return get_sales_by_product(
        ano=ano,
        mes=mes,
    )


def get_sales_by_customer_service(
    ano: int | None = None,
    mes: int | None = None,
):
    return get_sales_by_customer(
        ano=ano,
        mes=mes,
    )


def get_sales_by_month_service():
    return get_sales_by_month()

def get_available_years_service():
    return get_available_years()