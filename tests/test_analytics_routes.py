from fastapi.testclient import TestClient

from src.api.main import app


client = TestClient(app)


def test_get_sales_by_product():
    response = client.get(
        "/analytics/sales-by-product"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 20

    assert data[0]["id_produto"] == 1
    assert data[0]["nome_produto"] == "Notebook Dell"

    assert data[0]["quantidade_vendida"] == 3
    assert data[0]["receita"] == 10500
    assert data[0]["lucro"] == 2100


def test_get_sales_by_product_ordenado_por_receita():
    response = client.get(
        "/analytics/sales-by-product"
    )

    assert response.status_code == 200

    data = response.json()

    receitas = [
        registro["receita"]
        for registro in data
    ]

    assert receitas == sorted(
        receitas,
        reverse=True,
    )