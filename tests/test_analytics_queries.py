import pytest
from src.analytics.queries import (
    get_sales_by_product,
    get_sales_by_customer,
    get_sales_summary,
)
from decimal import Decimal

@pytest.mark.integration
def test_get_sales_by_product():
    resultado = get_sales_by_product()

    assert len(resultado) == 20

    assert resultado[0]["id_produto"] == 1
    assert resultado[0]["nome_produto"] == "Notebook Dell"

    assert resultado[0]["quantidade_vendida"] == 3
    assert resultado[0]["receita"] == 10500
    assert resultado[0]["lucro"] == 2100

@pytest.mark.integration
def test_get_sales_by_product_ordenado_por_receita():
    resultado = get_sales_by_product()

    receitas = [
        registro["receita"]
        for registro in resultado
    ]

    assert receitas == sorted(
        receitas,
        reverse=True,
    )

@pytest.mark.integration
def test_get_sales_by_customer():
    resultado = get_sales_by_customer()

    assert len(resultado) == 10

    assert resultado[0]["id_cliente"] == 1
    assert resultado[0]["nome_cliente"] == "Anderson Tecnologia"

    assert resultado[0]["quantidade_vendida"] == 6
    assert resultado[0]["receita"] == Decimal("11699.90")
    assert resultado[0]["lucro"] == Decimal("2469.90")


@pytest.mark.integration
def test_get_sales_by_customer_ordenado_por_receita():
    resultado = get_sales_by_customer()

    receitas = [
        registro["receita"]
        for registro in resultado
    ]

    assert receitas == sorted(
        receitas,
        reverse=True,
    )

@pytest.mark.integration
def test_get_sales_summary():
    resultado = get_sales_summary()

    assert resultado["quantidade_vendida"] == 40
    assert resultado["receita_total"] == 34169.50
    assert resultado["custo_total"] == 25340.00
    assert resultado["lucro_total"] == 8829.50
    assert resultado["margem"] ==  Decimal('25.84')