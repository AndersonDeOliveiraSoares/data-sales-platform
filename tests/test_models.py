from decimal import Decimal

from src.database.models.cliente import Cliente
from src.database.models.produto import Produto
from src.database.models.pedido import Pedido
from src.database.models.item_pedido import ItemPedido


def test_cliente_model():
    cliente = Cliente(
        nome="Cliente Teste",
        cpf_cnpj="12345678900",
        email="teste@example.com",
    )

    assert cliente.nome == "Cliente Teste"
    assert cliente.cpf_cnpj == "12345678900"
    assert cliente.email == "teste@example.com"

def test_produto_model():
    produto = Produto(
        nome_produto="Notebook",
        categoria="Eletrônicos",
        subcategoria="Informática",
        preco_venda=Decimal("3500.00"),
        preco_custo=Decimal("2800.00"),
        quantidade_estoque=10,
    )

    assert produto.nome_produto == "Notebook"
    assert produto.preco_venda == Decimal("3500.00")
    assert produto.preco_custo == Decimal("2800.00")
    assert produto.quantidade_estoque == 10

def test_pedido_model():
    pedido = Pedido(
        id_cliente=1,
        status_pedido="PENDENTE",
        valor_total=Decimal("3500.00"),
        valor_frete=Decimal("50.00"),
        forma_pagamento="PIX",
    )

    assert pedido.id_cliente == 1
    assert pedido.status_pedido == "PENDENTE"
    assert pedido.valor_total == Decimal("3500.00")
    assert pedido.valor_frete == Decimal("50.00")
    assert pedido.forma_pagamento == "PIX"

def test_item_pedido_model():
    item = ItemPedido(
        id_pedido=1,
        id_produto=10,
        quantidade=2,
        preco_unitario=Decimal("100.00"),
        subtotal=Decimal("200.00"),
    )

    assert item.id_pedido == 1
    assert item.id_produto == 10
    assert item.quantidade == 2
    assert item.preco_unitario == Decimal("100.00")
    assert item.subtotal == Decimal("200.00")