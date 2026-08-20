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


def test_create_cliente():
    response = client.post(
        "/clientes/",
        json={
            "nome": "Cliente API Teste",
            "cpf_cnpj": "11111111111",
            "email": "api1@example.com",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["nome"] == "Cliente API Teste"
    assert data["cpf_cnpj"] == "11111111111"
    assert data["email"] == "api1@example.com"


def test_create_cliente_duplicate():
    cliente = {
        "nome": "Cliente Duplicado",
        "cpf_cnpj": "22222222222",
        "email": "duplicado@example.com",
    }

    response_first = client.post(
        "/clientes/",
        json=cliente,
    )

    assert response_first.status_code == 201

    response_second = client.post(
        "/clientes/",
        json=cliente,
    )

    assert response_second.status_code == 409

    assert response_second.json() == {
        "detail": "CPF/CNPJ ou e-mail já cadastrado."
    }


def test_update_cliente():
    response_create = client.post(
        "/clientes/",
        json={
            "nome": "Cliente Original",
            "cpf_cnpj": "33333333333",
            "email": "original@example.com",
        },
    )

    assert response_create.status_code == 201

    cliente = response_create.json()
    id_cliente = cliente["id_cliente"]

    response_update = client.put(
        f"/clientes/{id_cliente}",
        json={
            "nome": "Cliente Atualizado",
            "cpf_cnpj": "44444444444",
            "email": "atualizado@example.com",
            "telefone": "21999999999",
            "endereco": "Rua Teste, 100",
            "cidade": "Rio de Janeiro",
            "estado": "RJ",
            "cep": "23000000",
        },
    )

    assert response_update.status_code == 200

    data = response_update.json()

    assert data["id_cliente"] == id_cliente
    assert data["nome"] == "Cliente Atualizado"
    assert data["cpf_cnpj"] == "44444444444"
    assert data["email"] == "atualizado@example.com"
    assert data["telefone"] == "21999999999"


def test_update_cliente_not_found():
    response = client.put(
        "/clientes/999999",
        json={
            "nome": "Cliente Inexistente",
            "cpf_cnpj": "55555555555",
            "email": "inexistente@example.com",
        },
    )

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Cliente não encontrado."
    }


def test_update_cliente_duplicate_cpf():
    response_first = client.post(
        "/clientes/",
        json={
            "nome": "Cliente CPF 1",
            "cpf_cnpj": "66666666666",
            "email": "cpf1@example.com",
        },
    )

    assert response_first.status_code == 201

    response_second = client.post(
        "/clientes/",
        json={
            "nome": "Cliente CPF 2",
            "cpf_cnpj": "77777777777",
            "email": "cpf2@example.com",
        },
    )

    assert response_second.status_code == 201

    cliente = response_second.json()
    id_cliente = cliente["id_cliente"]

    response_update = client.put(
        f"/clientes/{id_cliente}",
        json={
            "nome": "Cliente CPF 2 Atualizado",
            "cpf_cnpj": "66666666666",
            "email": "cpf2.novo@example.com",
        },
    )

    assert response_update.status_code == 409

    assert response_update.json() == {
        "detail": "CPF/CNPJ ou e-mail já cadastrado."
    }


def test_update_cliente_duplicate_email():
    response_first = client.post(
        "/clientes/",
        json={
            "nome": "Cliente Email 1",
            "cpf_cnpj": "88888888888",
            "email": "email1@example.com",
        },
    )

    assert response_first.status_code == 201

    response_second = client.post(
        "/clientes/",
        json={
            "nome": "Cliente Email 2",
            "cpf_cnpj": "99999999999",
            "email": "email2@example.com",
        },
    )

    assert response_second.status_code == 201

    cliente = response_second.json()
    id_cliente = cliente["id_cliente"]

    response_update = client.put(
        f"/clientes/{id_cliente}",
        json={
            "nome": "Cliente Email 2 Atualizado",
            "cpf_cnpj": "99999999998",
            "email": "email1@example.com",
        },
    )

    assert response_update.status_code == 409

    assert response_update.json() == {
        "detail": "CPF/CNPJ ou e-mail já cadastrado."
    }

def test_listar_clientes_paginado():
    response = client.get(
        "/clientes/?page=1&limit=10"
    )

    assert response.status_code == 200

    data = response.json()

    assert "items" in data
    assert "page" in data
    assert "limit" in data
    assert "total" in data
    assert "pages" in data

    assert data["page"] == 1
    assert data["limit"] == 10
    assert isinstance(data["items"], list)


def test_listar_clientes_page_zero():
    response = client.get(
        "/clientes/?page=0&limit=10"
    )

    assert response.status_code == 422


def test_listar_clientes_limit_zero():
    response = client.get(
        "/clientes/?page=1&limit=0"
    )

    assert response.status_code == 422


def test_listar_clientes_limit_maior_que_100():
    response = client.get(
        "/clientes/?page=1&limit=101"
    )

    assert response.status_code == 422


def test_buscar_cliente_inexistente():
    response = client.get(
        "/clientes/999999"
    )

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Cliente não encontrado."
    }


def test_excluir_cliente_inexistente():
    response = client.delete(
        "/clientes/999999"
    )

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Cliente não encontrado."
    }