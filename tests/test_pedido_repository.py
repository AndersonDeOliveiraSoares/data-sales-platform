from decimal import Decimal

from src.database.models.cliente import Cliente
from src.database.models.pedido import Pedido
from src.database.repositories.pedido_repository import PedidoRepository


def criar_cliente(db):
    cliente = Cliente(
        nome="Cliente Pedido Teste",
        cpf_cnpj="11111111111",
        email="cliente.pedido@example.com",
    )

    db.add(cliente)
    db.commit()
    db.refresh(cliente)

    return cliente


def test_create_pedido(db):
    repository = PedidoRepository(db)

    cliente = criar_cliente(db)

    pedido = Pedido(
        id_cliente=cliente.id_cliente,
        status_pedido="PENDENTE",
        valor_total=Decimal("3500.00"),
        valor_frete=Decimal("50.00"),
        forma_pagamento="PIX",
    )

    resultado = repository.create(pedido)

    assert resultado.id_pedido is not None
    assert resultado.id_cliente == cliente.id_cliente
    assert resultado.status_pedido == "PENDENTE"
    assert resultado.valor_total == Decimal("3500.00")
    assert resultado.valor_frete == Decimal("50.00")
    assert resultado.forma_pagamento == "PIX"


def test_get_by_id_pedido(db):
    repository = PedidoRepository(db)

    cliente = criar_cliente(db)

    pedido = Pedido(
        id_cliente=cliente.id_cliente,
        status_pedido="PAGO",
        valor_total=Decimal("1000.00"),
        valor_frete=Decimal("20.00"),
        forma_pagamento="CARTAO",
    )

    pedido_criado = repository.create(pedido)

    resultado = repository.get_by_id(pedido_criado.id_pedido)

    assert resultado is not None
    assert resultado.id_pedido == pedido_criado.id_pedido
    assert resultado.id_cliente == cliente.id_cliente
    assert resultado.status_pedido == "PAGO"


def test_get_all_pedidos(db):
    repository = PedidoRepository(db)

    cliente = criar_cliente(db)

    pedido1 = Pedido(
        id_cliente=cliente.id_cliente,
        status_pedido="PENDENTE",
        valor_total=Decimal("100.00"),
        valor_frete=Decimal("10.00"),
        forma_pagamento="PIX",
    )

    pedido2 = Pedido(
        id_cliente=cliente.id_cliente,
        status_pedido="PAGO",
        valor_total=Decimal("200.00"),
        valor_frete=Decimal("15.00"),
        forma_pagamento="CARTAO",
    )

    repository.create(pedido1)
    repository.create(pedido2)

    resultado = repository.get_all()

    assert len(resultado) >= 2
    assert any(
        pedido.status_pedido == "PENDENTE"
        for pedido in resultado
    )
    assert any(
        pedido.status_pedido == "PAGO"
        for pedido in resultado
    )


def test_delete_pedido(db):
    repository = PedidoRepository(db)

    cliente = criar_cliente(db)

    pedido = Pedido(
        id_cliente=cliente.id_cliente,
        status_pedido="CANCELADO",
        valor_total=Decimal("500.00"),
        valor_frete=Decimal("0.00"),
        forma_pagamento="PIX",
    )

    pedido_criado = repository.create(pedido)

    repository.delete(pedido_criado)

    resultado = repository.get_by_id(pedido_criado.id_pedido)

    assert resultado is None