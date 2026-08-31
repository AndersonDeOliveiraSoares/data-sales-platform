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

    assert data[0]["quantidade_vendida"] == 430
    assert data[0]["receita"] == 1505000.0
    assert data[0]["lucro"] == 301000.0


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

def test_get_sales_by_customer():
    response = client.get(
        "/analytics/sales-by-customer"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 10

    assert data[0]["id_cliente"] == 6
    assert data[0]["nome_cliente"] == "Ricardo Souza"

    assert data[0]["quantidade_vendida"] == 873
    assert data[0]["receita"] == 851342.8
    assert data[0]["lucro"] == 213942.8

def test_get_sales_by_customer_ordenado_por_receita():
    response = client.get(
        "/analytics/sales-by-customer"
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

def test_get_sales_summary():
    response = client.get(
        "/analytics/sales-summary"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["quantidade_vendida"] == 8439
    assert data["receita_total"] == 7475020.30
    assert data["custo_total"] == 5547000.0
    assert data["lucro_total"] == 1928020.3
    assert data["margem"] == 25.79