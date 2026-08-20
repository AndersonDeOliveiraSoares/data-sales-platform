from decimal import Decimal

from src.database.models.cliente import Cliente
from src.database.models.item_pedido import ItemPedido
from src.database.models.pedido import Pedido
from src.database.models.produto import Produto
from src.database.repositories.item_pedido_repository import ItemPedidoRepository


def criar_pedido_e_produto(db):
    cliente = Cliente(
        nome="Cliente Item Pedido",
        cpf_cnpj="22222222222",
        email="cliente.item@example.com",
    )

    db.add(cliente)
    db.commit()
    db.refresh(cliente)

    pedido = Pedido(
        id_cliente=cliente.id_cliente,
        status_pedido="PENDENTE",
        valor_total=Decimal("3500.00"),
        valor_frete=Decimal("50.00"),
        forma_pagamento="PIX",
    )

    db.add(pedido)
    db.commit()
    db.refresh(pedido)

    produto = Produto(
        nome_produto="Produto Item Pedido",
        categoria="Informática",
        subcategoria="Acessórios",
        preco_venda=Decimal("100.00"),
        preco_custo=Decimal("70.00"),
        quantidade_estoque=10,
    )

    db.add(produto)
    db.commit()
    db.refresh(produto)

    return pedido, produto


def test_create_item_pedido(db):
    repository = ItemPedidoRepository(db)

    pedido, produto = criar_pedido_e_produto(db)

    item = ItemPedido(
        id_pedido=pedido.id_pedido,
        id_produto=produto.id_produto,
        quantidade=2,
        preco_unitario=Decimal("100.00"),
        subtotal=Decimal("200.00"),
    )

    resultado = repository.create(item)

    assert resultado.id_item_pedido is not None
    assert resultado.id_pedido == pedido.id_pedido
    assert resultado.id_produto == produto.id_produto
    assert resultado.quantidade == 2
    assert resultado.preco_unitario == Decimal("100.00")
    assert resultado.subtotal == Decimal("200.00")


def test_get_by_id_item_pedido(db):
    repository = ItemPedidoRepository(db)

    pedido, produto = criar_pedido_e_produto(db)

    item = ItemPedido(
        id_pedido=pedido.id_pedido,
        id_produto=produto.id_produto,
        quantidade=3,
        preco_unitario=Decimal("50.00"),
        subtotal=Decimal("150.00"),
    )

    item_criado = repository.create(item)

    resultado = repository.get_by_id(item_criado.id_item_pedido)

    assert resultado is not None
    assert resultado.id_item_pedido == item_criado.id_item_pedido
    assert resultado.quantidade == 3
    assert resultado.subtotal == Decimal("150.00")


def test_get_all_itens_pedido(db):
    repository = ItemPedidoRepository(db)

    pedido, produto = criar_pedido_e_produto(db)

    item1 = ItemPedido(
        id_pedido=pedido.id_pedido,
        id_produto=produto.id_produto,
        quantidade=1,
        preco_unitario=Decimal("100.00"),
        subtotal=Decimal("100.00"),
    )

    item2 = ItemPedido(
        id_pedido=pedido.id_pedido,
        id_produto=produto.id_produto,
        quantidade=2,
        preco_unitario=Decimal("50.00"),
        subtotal=Decimal("100.00"),
    )

    repository.create(item1)
    repository.create(item2)

    resultado = repository.get_all()

    assert len(resultado) >= 2
    assert any(item.quantidade == 1 for item in resultado)
    assert any(item.quantidade == 2 for item in resultado)


def test_delete_item_pedido(db):
    repository = ItemPedidoRepository(db)

    pedido, produto = criar_pedido_e_produto(db)

    item = ItemPedido(
        id_pedido=pedido.id_pedido,
        id_produto=produto.id_produto,
        quantidade=1,
        preco_unitario=Decimal("100.00"),
        subtotal=Decimal("100.00"),
    )

    item_criado = repository.create(item)

    repository.delete(item_criado)

    resultado = repository.get_by_id(item_criado.id_item_pedido)

    assert resultado is None