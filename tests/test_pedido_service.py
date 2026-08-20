from decimal import Decimal
from uuid import uuid4

import pytest

from src.api.exceptions.handlers import (
    ClienteNotFoundException,
    EstoqueInsuficienteException,
    PedidoNotFoundException,
)
from src.api.schemas.pedido_schemas import (
    PedidoCreate,
    PedidoUpdate,
)
from src.database.models.cliente import Cliente
from src.database.models.item_pedido import ItemPedido
from src.database.models.pedido import Pedido
from src.database.models.produto import Produto
from src.services.pedido_service import PedidoService
from tests.conftest import SessionTest


# ============================================================
# HELPERS
# ============================================================


def criar_cliente(db):
    identificador = uuid4().hex[:10]

    cliente = Cliente(
        nome="Cliente Pedido Teste",
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
    quantidade_estoque=100,
):
    identificador = uuid4().hex[:10]

    produto = Produto(
        nome_produto=f"Produto Pedido Teste {identificador}",
        categoria="Categoria Teste",
        subcategoria="Subcategoria Teste",
        preco_venda=preco_venda,
        preco_custo=Decimal("50.00"),
        quantidade_estoque=quantidade_estoque,
    )

    db.add(produto)
    db.commit()
    db.refresh(produto)

    return produto


def criar_pedido(db, cliente=None):
    if cliente is None:
        cliente = criar_cliente(db)

    pedido = Pedido(
        id_cliente=cliente.id_cliente,
        valor_total=Decimal("100.00"),
        valor_frete=Decimal("10.00"),
        forma_pagamento="PIX",
    )

    db.add(pedido)
    db.commit()
    db.refresh(pedido)

    return pedido


# ============================================================
# CRIAR PEDIDO
# ============================================================


def test_criar_pedido():
    db = SessionTest()

    try:
        cliente = criar_cliente(db)

        produto = criar_produto(
            db,
            Decimal("100.00"),
        )

        service = PedidoService(db)

        pedido_data = PedidoCreate(
            id_cliente=cliente.id_cliente,
            valor_total=Decimal("0.00"),
            valor_frete=Decimal("10.00"),
            forma_pagamento="PIX",
            itens=[
                {
                    "id_produto": produto.id_produto,
                    "quantidade": 2,
                }
            ],
        )

        pedido = service.criar(pedido_data)

        assert pedido.id_pedido is not None
        assert pedido.id_cliente == cliente.id_cliente
        assert pedido.valor_total == Decimal("210.00")
        assert pedido.valor_frete == Decimal("10.00")
        assert pedido.forma_pagamento == "PIX"

    finally:
        db.close()


def test_criar_pedido_cliente_inexistente():
    db = SessionTest()

    try:
        produto = criar_produto(db)

        service = PedidoService(db)

        pedido_data = PedidoCreate(
            id_cliente=999999,
            valor_total=Decimal("0.00"),
            valor_frete=Decimal("10.00"),
            forma_pagamento="PIX",
            itens=[
                {
                    "id_produto": produto.id_produto,
                    "quantidade": 2,
                }
            ],
        )

        with pytest.raises(ClienteNotFoundException):
            service.criar(pedido_data)

    finally:
        db.close()


def test_criar_pedido_com_itens_calcula_valor_total():
    db = SessionTest()

    try:
        cliente = criar_cliente(db)

        produto1 = criar_produto(
            db,
            Decimal("100.00"),
        )

        produto2 = criar_produto(
            db,
            Decimal("50.00"),
        )

        service = PedidoService(db)

        pedido_data = PedidoCreate(
            id_cliente=cliente.id_cliente,
            itens=[
                {
                    "id_produto": produto1.id_produto,
                    "quantidade": 2,
                },
                {
                    "id_produto": produto2.id_produto,
                    "quantidade": 3,
                },
            ],
            valor_frete=Decimal("20.00"),
            forma_pagamento="PIX",
        )

        pedido = service.criar(pedido_data)

        assert pedido.id_pedido is not None

        # 100 * 2 = 200
        # 50 * 3 = 150
        # frete = 20
        # total = 370
        assert pedido.valor_total == Decimal("370.00")
        assert pedido.valor_frete == Decimal("20.00")

    finally:
        db.close()


# ============================================================
# ESTOQUE
# ============================================================


def test_criar_pedido_baixa_estoque():
    db = SessionTest()

    try:
        cliente = criar_cliente(db)

        produto = criar_produto(
            db,
            preco_venda=Decimal("100.00"),
            quantidade_estoque=10,
        )

        service = PedidoService(db)

        pedido_data = PedidoCreate(
            id_cliente=cliente.id_cliente,
            itens=[
                {
                    "id_produto": produto.id_produto,
                    "quantidade": 3,
                }
            ],
            valor_frete=Decimal("10.00"),
            forma_pagamento="PIX",
        )

        service.criar(pedido_data)

        db.refresh(produto)

        assert produto.quantidade_estoque == 7

    finally:
        db.close()


def test_criar_pedido_venda_exatamente_estoque():
    db = SessionTest()

    try:
        cliente = criar_cliente(db)

        produto = criar_produto(
            db,
            preco_venda=Decimal("100.00"),
            quantidade_estoque=5,
        )

        service = PedidoService(db)

        pedido_data = PedidoCreate(
            id_cliente=cliente.id_cliente,
            itens=[
                {
                    "id_produto": produto.id_produto,
                    "quantidade": 5,
                }
            ],
            valor_frete=Decimal("0.00"),
            forma_pagamento="PIX",
        )

        service.criar(pedido_data)

        db.refresh(produto)

        assert produto.quantidade_estoque == 0

    finally:
        db.close()


def test_criar_pedido_estoque_insuficiente():
    db = SessionTest()

    try:
        cliente = criar_cliente(db)

        produto = criar_produto(
            db,
            preco_venda=Decimal("100.00"),
            quantidade_estoque=2,
        )

        service = PedidoService(db)

        pedido_data = PedidoCreate(
            id_cliente=cliente.id_cliente,
            itens=[
                {
                    "id_produto": produto.id_produto,
                    "quantidade": 3,
                }
            ],
            valor_frete=Decimal("10.00"),
            forma_pagamento="PIX",
        )

        with pytest.raises(EstoqueInsuficienteException):
            service.criar(pedido_data)

        db.refresh(produto)

        assert produto.quantidade_estoque == 2

    finally:
        db.close()


def test_criar_pedido_rollback_quando_um_item_nao_tem_estoque():
    db = SessionTest()

    try:
        cliente = criar_cliente(db)

        produto1 = criar_produto(
            db,
            preco_venda=Decimal("100.00"),
            quantidade_estoque=10,
        )

        produto2 = criar_produto(
            db,
            preco_venda=Decimal("50.00"),
            quantidade_estoque=1,
        )

        service = PedidoService(db)

        pedido_data = PedidoCreate(
            id_cliente=cliente.id_cliente,
            itens=[
                {
                    "id_produto": produto1.id_produto,
                    "quantidade": 2,
                },
                {
                    "id_produto": produto2.id_produto,
                    "quantidade": 5,
                },
            ],
            valor_frete=Decimal("10.00"),
            forma_pagamento="PIX",
        )

        with pytest.raises(EstoqueInsuficienteException):
            service.criar(pedido_data)

        db.refresh(produto1)
        db.refresh(produto2)

        assert produto1.quantidade_estoque == 10
        assert produto2.quantidade_estoque == 1

        pedidos = (
            db.query(Pedido)
            .filter(
                Pedido.id_cliente == cliente.id_cliente
            )
            .all()
        )

        assert pedidos == []

    finally:
        db.close()


# ============================================================
# BUSCAR
# ============================================================


def test_buscar_pedido():
    db = SessionTest()

    try:
        pedido = criar_pedido(db)

        service = PedidoService(db)

        resultado = service.buscar_por_id(
            pedido.id_pedido
        )

        assert resultado.id_pedido == pedido.id_pedido
        assert resultado.id_cliente == pedido.id_cliente
        assert resultado.valor_total == Decimal("100.00")
        assert resultado.valor_frete == Decimal("10.00")

    finally:
        db.close()


def test_buscar_pedido_inexistente():
    db = SessionTest()

    try:
        service = PedidoService(db)

        with pytest.raises(PedidoNotFoundException):
            service.buscar_por_id(999999)

    finally:
        db.close()


# ============================================================
# LISTAR
# ============================================================


def test_listar_pedidos():
    db = SessionTest()

    try:
        cliente = criar_cliente(db)

        pedido1 = criar_pedido(db, cliente)
        pedido2 = criar_pedido(db, cliente)

        service = PedidoService(db)

        resultado = service.listar()

        ids = [
            pedido.id_pedido
            for pedido in resultado
        ]

        assert pedido1.id_pedido in ids
        assert pedido2.id_pedido in ids

    finally:
        db.close()


# ============================================================
# ATUALIZAR
# ============================================================


def test_atualizar_pedido():
    db = SessionTest()

    try:
        pedido = criar_pedido(db)

        service = PedidoService(db)

        pedido_data = PedidoUpdate(
            status_pedido="PAGO",
            valor_total=Decimal("200.00"),
            valor_frete=Decimal("20.00"),
            forma_pagamento="CARTAO",
        )

        resultado = service.atualizar(
            id_pedido=pedido.id_pedido,
            pedido_data=pedido_data,
        )

        assert resultado.status_pedido == "PAGO"
        assert resultado.valor_total == Decimal("20.00")
        assert resultado.valor_frete == Decimal("20.00")
        assert resultado.forma_pagamento == "CARTAO"

    finally:
        db.close()


def test_atualizar_pedido_inexistente():
    db = SessionTest()

    try:
        service = PedidoService(db)

        pedido_data = PedidoUpdate(
            status_pedido="PAGO",
            valor_total=Decimal("200.00"),
            valor_frete=Decimal("20.00"),
            forma_pagamento="PIX",
        )

        with pytest.raises(PedidoNotFoundException):
            service.atualizar(
                id_pedido=999999,
                pedido_data=pedido_data,
            )

    finally:
        db.close()


# ============================================================
# EXCLUIR
# ============================================================


def test_excluir_pedido():
    db = SessionTest()

    try:
        pedido = criar_pedido(db)

        id_pedido = pedido.id_pedido

        service = PedidoService(db)

        service.excluir(id_pedido)

        resultado = service.repository.get_by_id(
            id_pedido
        )

        assert resultado is None

    finally:
        db.close()


def test_excluir_pedido_inexistente():
    db = SessionTest()

    try:
        service = PedidoService(db)

        with pytest.raises(PedidoNotFoundException):
            service.excluir(999999)

    finally:
        db.close()


# ============================================================
# PAGINAÇÃO
# ============================================================


def test_listar_pedidos_paginado():
    db = SessionTest()

    try:
        cliente = criar_cliente(db)

        for _ in range(5):
            criar_pedido(db, cliente)

        service = PedidoService(db)

        resultado = service.listar_paginado(
            page=1,
            limit=2,
        )

        assert len(resultado["items"]) == 2
        assert resultado["page"] == 1
        assert resultado["limit"] == 2
        assert resultado["total"] >= 5
        assert resultado["pages"] >= 3

    finally:
        db.close()


def test_listar_pedidos_pagina_2():
    db = SessionTest()

    try:
        cliente = criar_cliente(db)

        for _ in range(5):
            criar_pedido(db, cliente)

        service = PedidoService(db)

        resultado = service.listar_paginado(
            page=2,
            limit=2,
        )

        assert len(resultado["items"]) == 2
        assert resultado["page"] == 2
        assert resultado["limit"] == 2
        assert resultado["total"] >= 5

    finally:
        db.close()


def test_listar_pedidos_pagina_sem_resultado():
    db = SessionTest()

    try:
        cliente = criar_cliente(db)

        criar_pedido(db, cliente)

        service = PedidoService(db)

        resultado = service.listar_paginado(
            page=999,
            limit=10,
        )

        assert resultado["items"] == []
        assert resultado["page"] == 999
        assert resultado["limit"] == 10
        assert resultado["total"] >= 1

    finally:
        db.close()

def test_criar_pedido_rollback_quando_baixa_de_estoque_falha(
    monkeypatch,
):
    db = SessionTest()

    try:
        cliente = criar_cliente(db)

        produto1 = criar_produto(
            db,
            preco_venda=Decimal("100.00"),
            quantidade_estoque=10,
        )

        produto2 = criar_produto(
            db,
            preco_venda=Decimal("50.00"),
            quantidade_estoque=10,
        )

        service = PedidoService(db)

        baixa_original = (
            service.produto_repository.baixar_estoque
        )

        contador = {"quantidade": 0}

        def baixar_estoque_com_falha(
            id_produto,
            quantidade,
        ):
            contador["quantidade"] += 1

            if contador["quantidade"] == 2:
                return False

            return baixa_original(
                id_produto,
                quantidade,
            )

        monkeypatch.setattr(
            service.produto_repository,
            "baixar_estoque",
            baixar_estoque_com_falha,
        )

        pedido_data = PedidoCreate(
            id_cliente=cliente.id_cliente,
            itens=[
                {
                    "id_produto": produto1.id_produto,
                    "quantidade": 2,
                },
                {
                    "id_produto": produto2.id_produto,
                    "quantidade": 3,
                },
            ],
            valor_frete=Decimal("10.00"),
            forma_pagamento="PIX",
        )

        with pytest.raises(
            EstoqueInsuficienteException
        ):
            service.criar(pedido_data)

        db.refresh(produto1)
        db.refresh(produto2)

        assert produto1.quantidade_estoque == 10
        assert produto2.quantidade_estoque == 10

        pedidos = (
            db.query(Pedido)
            .filter(
                Pedido.id_cliente == cliente.id_cliente
            )
            .all()
        )

        assert pedidos == []

        itens = (
            db.query(ItemPedido)
            .all()
        )

        assert itens == []

    finally:
        db.close()

def test_atualizar_pedido_recalcula_valor_total():
    db = SessionTest()

    try:
        cliente = criar_cliente(db)

        produto = criar_produto(
            db,
            preco_venda=Decimal("100.00"),
            quantidade_estoque=10,
        )

        service = PedidoService(db)

        pedido_data = PedidoCreate(
            id_cliente=cliente.id_cliente,
            itens=[
                {
                    "id_produto": produto.id_produto,
                    "quantidade": 2,
                }
            ],
            valor_frete=Decimal("10.00"),
            forma_pagamento="PIX",
        )

        pedido = service.criar(pedido_data)

        pedido_update = PedidoUpdate(
            status_pedido="PAGO",
            valor_total=Decimal("1.00"),
            valor_frete=Decimal("20.00"),
            forma_pagamento="CARTAO",
        )

        resultado = service.atualizar(
            id_pedido=pedido.id_pedido,
            pedido_data=pedido_update,
        )

        assert resultado.status_pedido == "PAGO"
        assert resultado.valor_frete == Decimal("20.00")
        assert resultado.forma_pagamento == "CARTAO"

        # O valor_total enviado pelo cliente deve ser ignorado.
        #
        # 2 x R$ 100,00 = R$ 200,00
        # Frete = R$ 20,00
        # Total = R$ 220,00
        assert resultado.valor_total == Decimal("220.00")

    finally:
        db.close()