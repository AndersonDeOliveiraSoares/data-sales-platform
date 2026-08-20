from decimal import Decimal

from src.database.models.cliente import Cliente
from src.database.models.item_pedido import ItemPedido
from src.database.models.pedido import Pedido
from src.database.models.produto import Produto
from src.database.repositories.item_pedido_repository import (
    ItemPedidoRepository,
)

from tests.conftest import SessionTest


def criar_cliente(db):
    cliente = Cliente(
        nome="Cliente Item Pedido",
        cpf_cnpj="99999999999",
        email="cliente.item.pedido@example.com",
    )

    db.add(cliente)
    db.commit()
    db.refresh(cliente)

    return cliente


def criar_pedido(db, id_cliente):
    pedido = Pedido(
        id_cliente=id_cliente,
        valor_total=Decimal("100.00"),
        valor_frete=Decimal("10.00"),
        forma_pagamento="PIX",
    )

    db.add(pedido)
    db.commit()
    db.refresh(pedido)

    return pedido


def criar_produto(db):
    produto = Produto(
        nome_produto="Produto Item Pedido",
        categoria="Categoria Teste",
        subcategoria="Subcategoria Teste",
        preco_venda=Decimal("50.00"),
        preco_custo=Decimal("30.00"),
        quantidade_estoque=100,
    )

    db.add(produto)
    db.commit()
    db.refresh(produto)

    return produto


def criar_item(db, id_pedido, id_produto):
    item = ItemPedido(
        id_pedido=id_pedido,
        id_produto=id_produto,
        quantidade=2,
        preco_unitario=Decimal("50.00"),
        subtotal=Decimal("100.00"),
    )

    db.add(item)
    db.commit()
    db.refresh(item)

    return item


def preparar_dados():
    db = SessionTest()

    cliente = criar_cliente(db)
    pedido = criar_pedido(db, cliente.id_cliente)
    produto = criar_produto(db)

    return db, pedido, produto


def test_create_item_pedido():
    db, pedido, produto = preparar_dados()

    try:
        repository = ItemPedidoRepository(db)

        item = ItemPedido(
            id_pedido=pedido.id_pedido,
            id_produto=produto.id_produto,
            quantidade=2,
            preco_unitario=Decimal("50.00"),
            subtotal=Decimal("100.00"),
        )

        resultado = repository.create(item)

        assert resultado.id_item_pedido is not None
        assert resultado.id_pedido == pedido.id_pedido
        assert resultado.id_produto == produto.id_produto
        assert resultado.quantidade == 2
        assert resultado.preco_unitario == Decimal("50.00")
        assert resultado.subtotal == Decimal("100.00")

    finally:
        db.close()


def test_get_by_id_item_pedido():
    db, pedido, produto = preparar_dados()

    try:
        item = criar_item(
            db,
            pedido.id_pedido,
            produto.id_produto,
        )

        repository = ItemPedidoRepository(db)

        resultado = repository.get_by_id(
            item.id_item_pedido
        )

        assert resultado is not None
        assert resultado.id_item_pedido == item.id_item_pedido
        assert resultado.id_pedido == pedido.id_pedido
        assert resultado.id_produto == produto.id_produto

    finally:
        db.close()


def test_get_by_id_item_pedido_inexistente():
    db = SessionTest()

    try:
        repository = ItemPedidoRepository(db)

        resultado = repository.get_by_id(999999)

        assert resultado is None

    finally:
        db.close()


def test_get_all_itens_pedido():
    db, pedido, produto = preparar_dados()

    try:
        criar_item(
            db,
            pedido.id_pedido,
            produto.id_produto,
        )

        criar_item(
            db,
            pedido.id_pedido,
            produto.id_produto,
        )

        repository = ItemPedidoRepository(db)

        resultado = repository.get_all()

        assert len(resultado) >= 2

    finally:
        db.close()


def test_get_by_pedido():
    db, pedido, produto = preparar_dados()

    try:
        criar_item(
            db,
            pedido.id_pedido,
            produto.id_produto,
        )

        criar_item(
            db,
            pedido.id_pedido,
            produto.id_produto,
        )

        repository = ItemPedidoRepository(db)

        resultado = repository.get_by_pedido(
            pedido.id_pedido
        )

        assert len(resultado) == 2

        for item in resultado:
            assert item.id_pedido == pedido.id_pedido

    finally:
        db.close()


def test_get_paginated_item_pedido():
    db, pedido, produto = preparar_dados()

    try:
        for _ in range(5):
            criar_item(
                db,
                pedido.id_pedido,
                produto.id_produto,
            )

        repository = ItemPedidoRepository(db)

        items, total = repository.get_paginated(
            page=1,
            limit=2,
        )

        assert len(items) == 2
        assert total >= 5

    finally:
        db.close()


def test_update_item_pedido():
    db, pedido, produto = preparar_dados()

    try:
        item = criar_item(
            db,
            pedido.id_pedido,
            produto.id_produto,
        )

        repository = ItemPedidoRepository(db)

        item.quantidade = 3
        item.preco_unitario = Decimal("50.00")
        item.subtotal = Decimal("150.00")

        resultado = repository.update(item)

        assert resultado.quantidade == 3
        assert resultado.preco_unitario == Decimal("50.00")
        assert resultado.subtotal == Decimal("150.00")

    finally:
        db.close()


def test_delete_item_pedido():
    db, pedido, produto = preparar_dados()

    try:
        item = criar_item(
            db,
            pedido.id_pedido,
            produto.id_produto,
        )

        repository = ItemPedidoRepository(db)

        repository.delete(item)

        resultado = repository.get_by_id(
            item.id_item_pedido
        )

        assert resultado is None

    finally:
        db.close()