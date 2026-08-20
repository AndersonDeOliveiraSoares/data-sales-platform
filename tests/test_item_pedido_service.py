from decimal import Decimal

import pytest

from src.api.exceptions.handlers import (
    ItemPedidoNotFoundException,
    PedidoNotFoundException,
    ProdutoNotFoundException,
)
from src.api.schemas.item_pedido_schemas import (
    ItemPedidoCreate,
    ItemPedidoUpdate,
)
from src.database.models.cliente import Cliente
from src.database.models.item_pedido import ItemPedido
from src.database.models.pedido import Pedido
from src.database.models.produto import Produto
from src.services.item_pedido_service import ItemPedidoService
from tests.conftest import SessionTest


def criar_cliente(db):
    cliente = Cliente(
        nome="Cliente Teste",
        cpf_cnpj="99999999999",
        email="cliente.item.pedido@example.com",
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
        nome_produto="Produto Teste",
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


def test_criar_item_pedido():
    db = SessionTest()

    try:
        produto = criar_produto(
            db,
            Decimal("100.00"),
        )

        pedido = criar_pedido(db)

        service = ItemPedidoService(db)

        item_data = ItemPedidoCreate(
            id_pedido=pedido.id_pedido,
            id_produto=produto.id_produto,
            quantidade=3,
        )

        item = service.criar(item_data)

        assert item.id_item_pedido is not None
        assert item.id_pedido == pedido.id_pedido
        assert item.id_produto == produto.id_produto
        assert item.quantidade == 3
        assert item.preco_unitario == Decimal("100.00")
        assert item.subtotal == Decimal("300.00")

    finally:
        db.close()


def test_criar_item_pedido_pedido_inexistente():
    db = SessionTest()

    try:
        produto = criar_produto(db)

        service = ItemPedidoService(db)

        item_data = ItemPedidoCreate(
            id_pedido=999999,
            id_produto=produto.id_produto,
            quantidade=2,
        )

        with pytest.raises(PedidoNotFoundException):
            service.criar(item_data)

    finally:
        db.close()


def test_criar_item_pedido_produto_inexistente():
    db = SessionTest()

    try:
        pedido = criar_pedido(db)

        service = ItemPedidoService(db)

        item_data = ItemPedidoCreate(
            id_pedido=pedido.id_pedido,
            id_produto=999999,
            quantidade=2,
        )

        with pytest.raises(ProdutoNotFoundException):
            service.criar(item_data)

    finally:
        db.close()


def test_buscar_item_pedido():
    db = SessionTest()

    try:
        produto = criar_produto(db)
        pedido = criar_pedido(db)

        item = ItemPedido(
            id_pedido=pedido.id_pedido,
            id_produto=produto.id_produto,
            quantidade=2,
            preco_unitario=produto.preco_venda,
            subtotal=Decimal("200.00"),
        )

        db.add(item)
        db.commit()
        db.refresh(item)

        service = ItemPedidoService(db)

        resultado = service.buscar_por_id(
            item.id_item_pedido
        )

        assert resultado.id_item_pedido == item.id_item_pedido

    finally:
        db.close()


def test_buscar_item_pedido_inexistente():
    db = SessionTest()

    try:
        service = ItemPedidoService(db)

        with pytest.raises(ItemPedidoNotFoundException):
            service.buscar_por_id(999999)

    finally:
        db.close()


def test_listar_itens_pedido():
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

        service = ItemPedidoService(db)

        resultado = service.listar_por_pedido(
            pedido.id_pedido
        )

        assert len(resultado) == 2

    finally:
        db.close()


def test_listar_itens_pedido_inexistente():
    db = SessionTest()

    try:
        service = ItemPedidoService(db)

        with pytest.raises(PedidoNotFoundException):
            service.listar_por_pedido(999999)

    finally:
        db.close()


def test_atualizar_item_pedido():
    db = SessionTest()

    try:
        produto = criar_produto(
            db,
            Decimal("80.00"),
        )

        pedido = criar_pedido(db)

        item = ItemPedido(
            id_pedido=pedido.id_pedido,
            id_produto=produto.id_produto,
            quantidade=2,
            preco_unitario=produto.preco_venda,
            subtotal=Decimal("160.00"),
        )

        db.add(item)
        db.commit()
        db.refresh(item)

        service = ItemPedidoService(db)

        item_data = ItemPedidoUpdate(
            quantidade=5,
        )

        resultado = service.atualizar(
            id_item_pedido=item.id_item_pedido,
            item_data=item_data,
        )

        assert resultado.quantidade == 5
        assert resultado.preco_unitario == Decimal("80.00")
        assert resultado.subtotal == Decimal("400.00")

    finally:
        db.close()


def test_atualizar_item_pedido_inexistente():
    db = SessionTest()

    try:
        service = ItemPedidoService(db)

        item_data = ItemPedidoUpdate(
            quantidade=5,
        )

        with pytest.raises(ItemPedidoNotFoundException):
            service.atualizar(
                id_item_pedido=999999,
                item_data=item_data,
            )

    finally:
        db.close()


def test_excluir_item_pedido():
    db = SessionTest()

    try:
        produto = criar_produto(db)
        pedido = criar_pedido(db)

        item = ItemPedido(
            id_pedido=pedido.id_pedido,
            id_produto=produto.id_produto,
            quantidade=2,
            preco_unitario=produto.preco_venda,
            subtotal=Decimal("200.00"),
        )

        db.add(item)
        db.commit()
        db.refresh(item)

        id_item = item.id_item_pedido

        service = ItemPedidoService(db)

        service.excluir(id_item)

        resultado = service.repository.get_by_id(id_item)

        assert resultado is None

    finally:
        db.close()


def test_excluir_item_pedido_inexistente():
    db = SessionTest()

    try:
        service = ItemPedidoService(db)

        with pytest.raises(ItemPedidoNotFoundException):
            service.excluir(999999)

    finally:
        db.close()