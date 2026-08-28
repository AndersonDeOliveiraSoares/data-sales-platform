import pytest

from src.analytics.queries import get_sales_by_product

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