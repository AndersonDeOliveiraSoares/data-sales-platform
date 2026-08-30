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

def test_get_sales_by_customer():
    response = client.get(
        "/analytics/sales-by-customer"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 10

    assert data[0]["id_cliente"] == 1
    assert data[0]["nome_cliente"] == "Anderson Tecnologia"

    assert data[0]["quantidade_vendida"] == 6
    assert data[0]["receita"] == 11699.90
    assert data[0]["lucro"] == 2469.90

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

    assert data["quantidade_vendida"] == 40
    assert data["receita_total"] == 34169.50
    assert data["custo_total"] == 25340.00
    assert data["lucro_total"] == 8829.50
    assert data["margem"] == 25.84