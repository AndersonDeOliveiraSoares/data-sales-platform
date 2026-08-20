from decimal import Decimal

import pytest

from src.api.exceptions.handlers import ProdutoNotFoundException
from src.api.schemas.produto_schemas import ProdutoCreate, ProdutoUpdate
from src.services.produto_service import ProdutoService

from tests.conftest import SessionTest


def test_criar_produto():
    db = SessionTest()

    try:
        service = ProdutoService(db)

        produto_data = ProdutoCreate(
            nome_produto="Produto Service Teste",
            categoria="Eletrônicos",
            subcategoria="Informática",
            preco_venda=Decimal("150.00"),
            preco_custo=Decimal("100.00"),
            quantidade_estoque=10,
        )

        produto = service.criar(produto_data)

        assert produto.id_produto is not None
        assert produto.nome_produto == "Produto Service Teste"
        assert produto.categoria == "Eletrônicos"
        assert produto.preco_venda == Decimal("150.00")
        assert produto.preco_custo == Decimal("100.00")
        assert produto.quantidade_estoque == 10

    finally:
        db.close()


def test_buscar_produto():
    db = SessionTest()

    try:
        service = ProdutoService(db)

        produto_data = ProdutoCreate(
            nome_produto="Produto Buscar",
            categoria="Teste",
            preco_venda=Decimal("50.00"),
            preco_custo=Decimal("30.00"),
            quantidade_estoque=5,
        )

        produto_criado = service.criar(produto_data)

        produto = service.buscar_por_id(
            produto_criado.id_produto
        )

        assert produto.id_produto == produto_criado.id_produto
        assert produto.nome_produto == "Produto Buscar"

    finally:
        db.close()


def test_buscar_produto_inexistente():
    db = SessionTest()

    try:
        service = ProdutoService(db)

        with pytest.raises(ProdutoNotFoundException):
            service.buscar_por_id(999999)

    finally:
        db.close()


def test_atualizar_produto():
    db = SessionTest()

    try:
        service = ProdutoService(db)

        produto_data = ProdutoCreate(
            nome_produto="Produto Original",
            categoria="Teste",
            preco_venda=Decimal("100.00"),
            preco_custo=Decimal("60.00"),
            quantidade_estoque=10,
        )

        produto = service.criar(produto_data)

        update_data = ProdutoUpdate(
            nome_produto="Produto Atualizado",
            categoria="Nova Categoria",
            subcategoria="Nova Subcategoria",
            preco_venda=Decimal("120.00"),
            preco_custo=Decimal("70.00"),
            quantidade_estoque=20,
        )

        produto_atualizado = service.atualizar(
            produto.id_produto,
            update_data,
        )

        assert produto_atualizado.nome_produto == "Produto Atualizado"
        assert produto_atualizado.categoria == "Nova Categoria"
        assert produto_atualizado.preco_venda == Decimal("120.00")
        assert produto_atualizado.preco_custo == Decimal("70.00")
        assert produto_atualizado.quantidade_estoque == 20

    finally:
        db.close()


def test_excluir_produto():
    db = SessionTest()

    try:
        service = ProdutoService(db)

        produto_data = ProdutoCreate(
            nome_produto="Produto Excluir",
            categoria="Teste",
            preco_venda=Decimal("80.00"),
            preco_custo=Decimal("40.00"),
            quantidade_estoque=5,
        )

        produto = service.criar(produto_data)

        service.excluir(produto.id_produto)

        with pytest.raises(ProdutoNotFoundException):
            service.buscar_por_id(produto.id_produto)

    finally:
        db.close()