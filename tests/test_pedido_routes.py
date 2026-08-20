from decimal import Decimal
from uuid import uuid4

from fastapi.testclient import TestClient

from src.api.main import app
from src.database.connection import get_db
from src.database.models.cliente import Cliente
from src.database.models.pedido import Pedido
from src.database.models.produto import Produto
from src.database.models.item_pedido import ItemPedido
from tests.conftest import SessionTest


def override_get_db():
    db = SessionTest()

    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def criar_cliente():
    db = SessionTest()

    try:
        identificador = uuid4().hex[:10]

        cliente = Cliente(
            nome="Cliente API Pedido",
            cpf_cnpj=f"8{identificador}",
            email=f"cliente.{identificador}@example.com",
        )

        db.add(cliente)
        db.commit()
        db.refresh(cliente)

        return cliente.id_cliente

    finally:
        db.close()


def criar_produto(
    preco_venda=Decimal("100.00"),
):
    db = SessionTest()

    try:
        produto = Produto(
            nome_produto="Produto API Pedido",
            categoria="Categoria Teste",
            subcategoria="Subcategoria Teste",
            preco_venda=preco_venda,
            preco_custo=Decimal("50.00"),
            quantidade_estoque=100,
        )

        db.add(produto)
        db.commit()
        db.refresh(produto)

        return produto.id_produto

    finally:
        db.close()


def criar_pedido(id_cliente):
    db = SessionTest()

    try:
        pedido = Pedido(
            id_cliente=id_cliente,
            valor_total=Decimal("100.00"),
            valor_frete=Decimal("10.00"),
            forma_pagamento="PIX",
        )

        db.add(pedido)
        db.commit()
        db.refresh(pedido)

        return pedido.id_pedido

    finally:
        db.close()


def test_create_pedido():
    id_cliente = criar_cliente()
    id_produto = criar_produto(
        Decimal("100.00"),
    )

    response = client.post(
        "/pedidos/",
        json={
            "id_cliente": id_cliente,
            "valor_total": 0.00,
            "valor_frete": 20.00,
            "forma_pagamento": "PIX",
            "itens": [
                {
                    "id_produto": id_produto,
                    "quantidade": 2,
                }
            ],
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id_cliente"] == id_cliente

    # R$ 100,00 x 2 + R$ 20,00 de frete
    assert float(data["valor_total"]) == 220.00

    assert float(data["valor_frete"]) == 20.00
    assert data["forma_pagamento"] == "PIX"
    assert data["status_pedido"] == "PENDENTE"


def test_create_pedido_estoque_insuficiente():
    id_cliente = criar_cliente()
    id_produto = criar_produto()

    db = SessionTest()

    try:
        produto = db.get(
            Produto,
            id_produto,
        )

        produto.quantidade_estoque = 2

        db.commit()

    finally:
        db.close()

    response = client.post(
        "/pedidos/",
        json={
            "id_cliente": id_cliente,
            "valor_total": 0.00,
            "valor_frete": 10.00,
            "forma_pagamento": "PIX",
            "itens": [
                {
                    "id_produto": id_produto,
                    "quantidade": 3,
                }
            ],
        },
    )

    assert response.status_code == 400

    assert response.json() == {
        "detail": (
            "Estoque insuficiente para o produto "
            "'Produto API Pedido'. "
            "Disponível: 2. "
            "Solicitado: 3."
        )
    }


def test_create_pedido_cliente_inexistente():
    id_produto = criar_produto()

    response = client.post(
        "/pedidos/",
        json={
            "id_cliente": 999999,
            "valor_total": 0.00,
            "valor_frete": 10.00,
            "forma_pagamento": "PIX",
            "itens": [
                {
                    "id_produto": id_produto,
                    "quantidade": 2,
                }
            ],
        },
    )

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Cliente não encontrado."
    }


def test_create_pedido_produto_inexistente():
    id_cliente = criar_cliente()

    response = client.post(
        "/pedidos/",
        json={
            "id_cliente": id_cliente,
            "valor_total": 0.00,
            "valor_frete": 10.00,
            "forma_pagamento": "PIX",
            "itens": [
                {
                    "id_produto": 999999,
                    "quantidade": 2,
                }
            ],
        },
    )

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Produto não encontrado."
    }


def test_create_pedido_sem_itens():
    id_cliente = criar_cliente()

    response = client.post(
        "/pedidos/",
        json={
            "id_cliente": id_cliente,
            "valor_total": 0.00,
            "valor_frete": 10.00,
            "forma_pagamento": "PIX",
        },
    )

    assert response.status_code == 422


def test_get_pedidos():
    id_cliente = criar_cliente()

    criar_pedido(id_cliente)
    criar_pedido(id_cliente)

    response = client.get(
        "/pedidos/?page=1&limit=10"
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
    assert data["total"] >= 2


def test_get_pedido_by_id():
    id_cliente = criar_cliente()
    id_pedido = criar_pedido(id_cliente)

    response = client.get(
        f"/pedidos/{id_pedido}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id_pedido"] == id_pedido
    assert data["id_cliente"] == id_cliente


def test_get_pedido_inexistente():
    response = client.get(
        "/pedidos/999999"
    )

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Pedido não encontrado."
    }


def test_update_pedido():
    id_cliente = criar_cliente()
    id_pedido = criar_pedido(id_cliente)

    response = client.put(
        f"/pedidos/{id_pedido}",
        json={
            "status_pedido": "FINALIZADO",
            "valor_total": 200.00,
            "valor_frete": 15.00,
            "forma_pagamento": "CARTAO",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id_pedido"] == id_pedido
    assert data["status_pedido"] == "FINALIZADO"
    assert float(data["valor_total"]) == 200.00
    assert float(data["valor_frete"]) == 15.00
    assert data["forma_pagamento"] == "CARTAO"


def test_update_pedido_inexistente():
    response = client.put(
        "/pedidos/999999",
        json={
            "status_pedido": "FINALIZADO",
            "valor_total": 200.00,
            "valor_frete": 15.00,
            "forma_pagamento": "PIX",
        },
    )

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Pedido não encontrado."
    }


def test_delete_pedido():
    id_cliente = criar_cliente()
    id_pedido = criar_pedido(id_cliente)

    response = client.delete(
        f"/pedidos/{id_pedido}"
    )

    assert response.status_code == 204
    assert response.content == b""


def test_delete_pedido_inexistente():
    response = client.delete(
        "/pedidos/999999"
    )

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Pedido não encontrado."
    }


def test_paginacao_pedido():
    id_cliente = criar_cliente()

    for _ in range(5):
        criar_pedido(id_cliente)

    response = client.get(
        "/pedidos/?page=1&limit=2"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["page"] == 1
    assert data["limit"] == 2
    assert len(data["items"]) == 2
    assert data["total"] >= 5
    assert data["pages"] >= 3


def test_paginacao_page_zero():
    response = client.get(
        "/pedidos/?page=0&limit=10"
    )

    assert response.status_code == 422


def test_paginacao_limit_zero():
    response = client.get(
        "/pedidos/?page=1&limit=0"
    )

    assert response.status_code == 422


def test_paginacao_limit_maior_que_100():
    response = client.get(
        "/pedidos/?page=1&limit=101"
    )

    assert response.status_code == 422

def test_create_pedido_rollback_estoque_insuficiente():
    id_cliente = criar_cliente()

    db = SessionTest()

    try:
        produto1 = Produto(
            nome_produto="Produto Rollback 1",
            categoria="Teste",
            subcategoria="Teste",
            preco_venda=Decimal("100.00"),
            preco_custo=Decimal("50.00"),
            quantidade_estoque=10,
        )

        produto2 = Produto(
            nome_produto="Produto Rollback 2",
            categoria="Teste",
            subcategoria="Teste",
            preco_venda=Decimal("50.00"),
            preco_custo=Decimal("25.00"),
            quantidade_estoque=1,
        )

        db.add_all([produto1, produto2])
        db.commit()

        db.refresh(produto1)
        db.refresh(produto2)

        id_produto1 = produto1.id_produto
        id_produto2 = produto2.id_produto

    finally:
        db.close()

    response = client.post(
        "/pedidos/",
        json={
            "id_cliente": id_cliente,
            "valor_total": 0.00,
            "valor_frete": 10.00,
            "forma_pagamento": "PIX",
            "itens": [
                {
                    "id_produto": id_produto1,
                    "quantidade": 2,
                },
                {
                    "id_produto": id_produto2,
                    "quantidade": 5,
                },
            ],
        },
    )

    assert response.status_code == 400

    # Verifica estoque após o rollback
    db = SessionTest()

    try:
        produto1_atualizado = db.get(
            Produto,
            id_produto1,
        )

        produto2_atualizado = db.get(
            Produto,
            id_produto2,
        )

        assert produto1_atualizado.quantidade_estoque == 10
        assert produto2_atualizado.quantidade_estoque == 1

        # Verifica que nenhum pedido foi criado
        pedidos = (
            db.query(Pedido)
            .filter(
                Pedido.id_cliente == id_cliente
            )
            .all()
        )

        assert pedidos == []

    finally:
        db.close()

def test_update_pedido():
    id_cliente = criar_cliente()
    id_produto = criar_produto(
        Decimal("100.00"),
    )

    id_pedido = criar_pedido(id_cliente)

    db = SessionTest()

    try:
        item = ItemPedido(
            id_pedido=id_pedido,
            id_produto=id_produto,
            quantidade=2,
            preco_unitario=Decimal("100.00"),
            subtotal=Decimal("200.00"),
        )

        db.add(item)
        db.commit()

    finally:
        db.close()

    response = client.put(
        f"/pedidos/{id_pedido}",
        json={
            "status_pedido": "FINALIZADO",
            "valor_total": 1.00,
            "valor_frete": 15.00,
            "forma_pagamento": "CARTAO",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id_pedido"] == id_pedido
    assert data["status_pedido"] == "FINALIZADO"

    # O valor_total enviado pelo cliente é ignorado.
    #
    # 2 x R$ 100,00 = R$ 200,00
    # Frete = R$ 15,00
    # Total = R$ 215,00
    assert float(data["valor_total"]) == 215.00

    assert float(data["valor_frete"]) == 15.00
    assert data["forma_pagamento"] == "CARTAO"