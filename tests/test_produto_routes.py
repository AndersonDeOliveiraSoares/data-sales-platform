from fastapi.testclient import TestClient

from src.api.main import app
from src.database.connection import get_db

from tests.conftest import SessionTest


def override_get_db():
    db = SessionTest()

    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def criar_produto():
    response = client.post(
        "/produtos/",
        json={
            "nome_produto": "Produto API Teste",
            "categoria": "Informática",
            "subcategoria": "Notebook",
            "preco_venda": 3500.00,
            "preco_custo": 2800.00,
            "quantidade_estoque": 10,
        },
    )

    assert response.status_code == 201

    return response.json()


def test_create_produto():
    data = criar_produto()

    assert data["id_produto"] is not None
    assert data["nome_produto"] == "Produto API Teste"
    assert data["categoria"] == "Informática"
    assert data["preco_venda"] == "3500.00"
    assert data["preco_custo"] == "2800.00"
    assert data["quantidade_estoque"] == 10


def test_get_produto():
    produto = criar_produto()

    response = client.get(
        f"/produtos/{produto['id_produto']}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id_produto"] == produto["id_produto"]
    assert data["nome_produto"] == "Produto API Teste"


def test_get_produto_inexistente():
    response = client.get("/produtos/999999")

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Produto não encontrado."
    }


def test_update_produto():
    produto = criar_produto()

    response = client.put(
        f"/produtos/{produto['id_produto']}",
        json={
            "nome_produto": "Produto Atualizado",
            "categoria": "Eletrônicos",
            "subcategoria": "Notebook",
            "preco_venda": 4200.00,
            "preco_custo": 3200.00,
            "quantidade_estoque": 20,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["nome_produto"] == "Produto Atualizado"
    assert data["categoria"] == "Eletrônicos"
    assert data["preco_venda"] == "4200.00"
    assert data["preco_custo"] == "3200.00"
    assert data["quantidade_estoque"] == 20


def test_update_produto_inexistente():
    response = client.put(
        "/produtos/999999",
        json={
            "nome_produto": "Produto Atualizado",
            "categoria": "Eletrônicos",
            "subcategoria": "Notebook",
            "preco_venda": 4200.00,
            "preco_custo": 3200.00,
            "quantidade_estoque": 20,
        },
    )

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Produto não encontrado."
    }


def test_delete_produto():
    produto = criar_produto()

    response = client.delete(
        f"/produtos/{produto['id_produto']}"
    )

    assert response.status_code == 204

    response_get = client.get(
        f"/produtos/{produto['id_produto']}"
    )

    assert response_get.status_code == 404


def test_delete_produto_inexistente():
    response = client.delete("/produtos/999999")

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Produto não encontrado."
    }


def test_listar_produtos():
    criar_produto()

    response = client.get("/produtos/")

    assert response.status_code == 200

    data = response.json()

    assert "items" in data
    assert "page" in data
    assert "limit" in data
    assert "total" in data
    assert "pages" in data

    assert data["page"] == 1
    assert data["limit"] == 10
    assert data["total"] >= 1


def test_paginacao_produtos():
    for i in range(3):
        client.post(
            "/produtos/",
            json={
                "nome_produto": f"Produto Paginação {i}",
                "categoria": "Teste",
                "subcategoria": "Teste",
                "preco_venda": 100.00,
                "preco_custo": 50.00,
                "quantidade_estoque": 10,
            },
        )

    response = client.get(
        "/produtos/?page=1&limit=2"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["page"] == 1
    assert data["limit"] == 2
    assert len(data["items"]) <= 2


def test_page_zero():
    response = client.get(
        "/produtos/?page=0"
    )

    assert response.status_code == 422


def test_limit_zero():
    response = client.get(
        "/produtos/?limit=0"
    )

    assert response.status_code == 422


def test_limit_maior_que_100():
    response = client.get(
        "/produtos/?limit=101"
    )

    assert response.status_code == 422