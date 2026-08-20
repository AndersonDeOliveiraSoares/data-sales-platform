from decimal import Decimal

from fastapi.testclient import TestClient

from src.api.main import app
from src.database.connection import get_db
from src.database.models.cliente import Cliente
from src.database.models.item_pedido import ItemPedido
from src.database.models.pedido import Pedido
from src.database.models.produto import Produto
from tests.conftest import SessionTest


def override_get_db():
    db = SessionTest()

    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def criar_cliente(db):
    import uuid

    identificador = uuid.uuid4().hex[:10]

    cliente = Cliente(
        nome="Cliente API Item Pedido",
        cpf_cnpj=identificador,
        email=f"cliente.{identificador}@example.com",
    )

    db.add(cliente)
    db.commit()
    db.refresh(cliente)

    return cliente

def criar_produto(
    db,
    preco_venda=Decimal("100.00"),
):
    produto = Produto(
        nome_produto="Produto API Item Pedido",
        categoria="Categoria Teste",
        subcategoria="Subcategoria Teste",
        preco_venda=preco_venda,
        preco_custo=Decimal("50.00"),
        quantidade_estoque=100,
    )

    db.add(produto)
    db.commit()
    db.refresh(produto)

    return produto


def criar_pedido(db):
    cliente = criar_cliente(db)

    pedido = Pedido(
        id_cliente=cliente.id_cliente,
        valor_total=Decimal("0.00"),
        valor_frete=Decimal("0.00"),
        forma_pagamento="PIX",
    )

    db.add(pedido)
    db.commit()
    db.refresh(pedido)

    return pedido


def criar_item(
    db,
    quantidade=2,
    preco=Decimal("100.00"),
):
    produto = criar_produto(
        db,
        preco,
    )

    pedido = criar_pedido(db)

    item = ItemPedido(
        id_pedido=pedido.id_pedido,
        id_produto=produto.id_produto,
        quantidade=quantidade,
        preco_unitario=preco,
        subtotal=preco * quantidade,
    )

    db.add(item)
    db.commit()
    db.refresh(item)

    return item


def test_criar_item_pedido():
    db = SessionTest()

    try:
        produto = criar_produto(db)
        pedido = criar_pedido(db)

        response = client.post(
            "/itens-pedido/",
            json={
                "id_pedido": pedido.id_pedido,
                "id_produto": produto.id_produto,
                "quantidade": 3,
            },
        )

        assert response.status_code == 201

        data = response.json()

        assert data["id_pedido"] == pedido.id_pedido
        assert data["id_produto"] == produto.id_produto
        assert data["quantidade"] == 3
        assert Decimal(data["preco_unitario"]) == Decimal("100.00")
        assert Decimal(data["subtotal"]) == Decimal("300.00")

    finally:
        db.close()


def test_criar_item_pedido_pedido_inexistente():
    db = SessionTest()

    try:
        produto = criar_produto(db)

        response = client.post(
            "/itens-pedido/",
            json={
                "id_pedido": 999999,
                "id_produto": produto.id_produto,
                "quantidade": 2,
            },
        )

        assert response.status_code == 404

        assert response.json() == {
            "detail": "Pedido não encontrado."
        }

    finally:
        db.close()


def test_criar_item_pedido_produto_inexistente():
    db = SessionTest()

    try:
        pedido = criar_pedido(db)

        response = client.post(
            "/itens-pedido/",
            json={
                "id_pedido": pedido.id_pedido,
                "id_produto": 999999,
                "quantidade": 2,
            },
        )

        assert response.status_code == 404

        assert response.json() == {
            "detail": "Produto não encontrado."
        }

    finally:
        db.close()


def test_listar_itens_pedido():
    db = SessionTest()

    try:
        criar_item(db, quantidade=1)
        criar_item(db, quantidade=2)

        response = client.get(
            "/itens-pedido/"
        )

        assert response.status_code == 200

        data = response.json()

        assert "items" in data
        assert "page" in data
        assert "limit" in data
        assert "total" in data
        assert "pages" in data

        assert data["total"] >= 2

    finally:
        db.close()


def test_listar_itens_pedido_paginacao():
    db = SessionTest()

    try:
        for _ in range(3):
            criar_item(db)

        response = client.get(
            "/itens-pedido/?page=1&limit=2"
        )

        assert response.status_code == 200

        data = response.json()

        assert data["page"] == 1
        assert data["limit"] == 2
        assert len(data["items"]) <= 2

    finally:
        db.close()


def test_listar_itens_pedido_page_zero():
    response = client.get(
        "/itens-pedido/?page=0"
    )

    assert response.status_code == 422


def test_listar_itens_pedido_limit_zero():
    response = client.get(
        "/itens-pedido/?limit=0"
    )

    assert response.status_code == 422


def test_listar_itens_pedido_limit_maior_que_100():
    response = client.get(
        "/itens-pedido/?limit=101"
    )

    assert response.status_code == 422


def test_buscar_item_pedido():
    db = SessionTest()

    try:
        item = criar_item(db)

        response = client.get(
            f"/itens-pedido/{item.id_item_pedido}"
        )

        assert response.status_code == 200

        data = response.json()

        assert data["id_item_pedido"] == item.id_item_pedido
        assert data["id_pedido"] == item.id_pedido
        assert data["id_produto"] == item.id_produto

    finally:
        db.close()


def test_buscar_item_pedido_inexistente():
    response = client.get(
        "/itens-pedido/999999"
    )

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Item do pedido não encontrado."
    }


def test_listar_itens_por_pedido():
    db = SessionTest()

    try:
        produto = criar_produto(db)
        pedido = criar_pedido(db)

        item1 = ItemPedido(
            id_pedido=pedido.id_pedido,
            id_produto=produto.id_produto,
            quantidade=1,
            preco_unitario=produto.preco_venda,
            subtotal=Decimal("100.00"),
        )

        item2 = ItemPedido(
            id_pedido=pedido.id_pedido,
            id_produto=produto.id_produto,
            quantidade=2,
            preco_unitario=produto.preco_venda,
            subtotal=Decimal("200.00"),
        )

        db.add_all([item1, item2])
        db.commit()

        response = client.get(
            f"/itens-pedido/pedido/{pedido.id_pedido}"
        )

        assert response.status_code == 200

        data = response.json()

        assert len(data) == 2
        assert data[0]["id_pedido"] == pedido.id_pedido
        assert data[1]["id_pedido"] == pedido.id_pedido

    finally:
        db.close()


def test_listar_itens_por_pedido_inexistente():
    response = client.get(
        "/itens-pedido/pedido/999999"
    )

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Pedido não encontrado."
    }


def test_atualizar_item_pedido():
    db = SessionTest()

    try:
        item = criar_item(
            db,
            quantidade=2,
            preco=Decimal("80.00"),
        )

        response = client.put(
            f"/itens-pedido/{item.id_item_pedido}",
            json={
                "quantidade": 5,
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert data["quantidade"] == 5
        assert Decimal(data["preco_unitario"]) == Decimal("80.00")
        assert Decimal(data["subtotal"]) == Decimal("400.00")

    finally:
        db.close()


def test_atualizar_item_pedido_inexistente():
    response = client.put(
        "/itens-pedido/999999",
        json={
            "quantidade": 5,
        },
    )

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Item do pedido não encontrado."
    }


def test_atualizar_item_pedido_quantidade_invalida():
    db = SessionTest()

    try:
        item = criar_item(db)

        response = client.put(
            f"/itens-pedido/{item.id_item_pedido}",
            json={
                "quantidade": 0,
            },
        )

        assert response.status_code == 422

    finally:
        db.close()


def test_excluir_item_pedido():
    db = SessionTest()

    try:
        item = criar_item(db)

        response = client.delete(
            f"/itens-pedido/{item.id_item_pedido}"
        )

        assert response.status_code == 204

    finally:
        db.close()


def test_excluir_item_pedido_inexistente():
    response = client.delete(
        "/itens-pedido/999999"
    )

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Item do pedido não encontrado."
    }