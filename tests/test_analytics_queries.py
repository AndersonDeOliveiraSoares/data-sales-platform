import pytest
from src.analytics.queries import (
    get_sales_by_product,
    get_sales_by_customer,
    get_sales_summary,
    get_sales_by_month,
)
from decimal import Decimal

@pytest.mark.integration
def test_get_sales_by_product():
    resultado = get_sales_by_product()

    assert len(resultado) == 20

    assert resultado[0]["id_produto"] == 1
    assert resultado[0]["nome_produto"] == "Notebook Dell"

    assert resultado[0]["quantidade_vendida"] == 430
    assert resultado[0]["receita"] ==  Decimal("1505000.00")
    assert resultado[0]["lucro"] ==  Decimal("301000.00")

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

    assert resultado[0]["id_cliente"] == 6
    assert resultado[0]["nome_cliente"] == "Ricardo Souza"

    assert resultado[0]["quantidade_vendida"] == 873
    assert resultado[0]["receita"] == Decimal("851342.80")
    assert resultado[0]["lucro"] == Decimal("213942.80")


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

    assert resultado["quantidade_vendida"] == 8439
    assert resultado["receita_total"] ==  Decimal("7475020.30")
    assert resultado["custo_total"] ==  Decimal("5547000.00")
    assert resultado["lucro_total"] ==  Decimal("1928020.30")
    assert resultado["margem"] ==  Decimal('25.79')

@pytest.mark.integration
def test_get_sales_by_month():
    resultado = get_sales_by_month()

    assert len(resultado) == 24

    assert resultado[0]["ano"] == 2024
    assert resultado[0]["mes"] == 9

    assert resultado[0]["quantidade_vendida"] == 248
    assert resultado[0]["receita"] == Decimal("220708.70")
    assert resultado[0]["custo"] ==  Decimal("164120.00")
    assert resultado[0]["lucro"] ==  Decimal("56588.70")

@pytest.mark.integration
def test_get_sales_summary_filtrado_por_periodo():
    resultado = get_sales_summary(
        ano=2026,
        mes=8,
    )

    assert resultado["quantidade_vendida"] == 278
    assert resultado["receita_total"] ==  Decimal("265976.60")
    assert resultado["custo_total"] == Decimal('198820.00')
    assert resultado["lucro_total"] ==  Decimal('67156.60')
    assert resultado["margem"] == Decimal("25.25")


@pytest.mark.integration
def test_get_sales_by_product_filtrado_por_periodo():
    resultado = get_sales_by_product(
        ano=2026,
        mes=8,
    )

    assert len(resultado) == 20
    assert resultado[0]["id_produto"] == 1
    assert resultado[0]["nome_produto"] == "Notebook Dell"


@pytest.mark.integration
def test_get_sales_by_product_periodo_sem_vendas():
    resultado = get_sales_by_product(
        ano=2026,
        mes=7,
    )

    assert len(resultado) == 20