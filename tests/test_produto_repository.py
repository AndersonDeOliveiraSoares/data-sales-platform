from decimal import Decimal

from src.database.models.produto import Produto
from src.database.repositories.produto_repository import ProdutoRepository


def test_create_produto(db):
    repository = ProdutoRepository(db)

    produto = Produto(
        nome_produto="Notebook Repository Teste",
        categoria="Eletrônicos",
        subcategoria="Informática",
        preco_venda=Decimal("3500.00"),
        preco_custo=Decimal("2800.00"),
        quantidade_estoque=10,
    )

    resultado = repository.create(produto)

    assert resultado.id_produto is not None
    assert resultado.nome_produto == "Notebook Repository Teste"
    assert resultado.preco_venda == Decimal("3500.00")
    assert resultado.preco_custo == Decimal("2800.00")
    assert resultado.quantidade_estoque == 10


def test_get_by_id_produto(db):
    repository = ProdutoRepository(db)

    produto = Produto(
        nome_produto="Produto Busca",
        categoria="Informática",
        subcategoria="Acessórios",
        preco_venda=Decimal("150.00"),
        preco_custo=Decimal("100.00"),
        quantidade_estoque=20,
    )

    produto_criado = repository.create(produto)

    resultado = repository.get_by_id(produto_criado.id_produto)

    assert resultado is not None
    assert resultado.id_produto == produto_criado.id_produto
    assert resultado.nome_produto == "Produto Busca"


def test_get_all_produtos(db):
    repository = ProdutoRepository(db)

    produto1 = Produto(
        nome_produto="Produto Lista 1",
        categoria="Informática",
        preco_venda=Decimal("100.00"),
        preco_custo=Decimal("70.00"),
        quantidade_estoque=5,
    )

    produto2 = Produto(
        nome_produto="Produto Lista 2",
        categoria="Eletrônicos",
        preco_venda=Decimal("200.00"),
        preco_custo=Decimal("150.00"),
        quantidade_estoque=8,
    )

    repository.create(produto1)
    repository.create(produto2)

    resultado = repository.get_all()

    assert len(resultado) >= 2
    assert any(
        produto.nome_produto == "Produto Lista 1"
        for produto in resultado
    )
    assert any(
        produto.nome_produto == "Produto Lista 2"
        for produto in resultado
    )


def test_delete_produto(db):
    repository = ProdutoRepository(db)

    produto = Produto(
        nome_produto="Produto Excluir",
        categoria="Teste",
        preco_venda=Decimal("50.00"),
        preco_custo=Decimal("30.00"),
        quantidade_estoque=1,
    )

    produto_criado = repository.create(produto)

    repository.delete(produto_criado)

    resultado = repository.get_by_id(produto_criado.id_produto)

    assert resultado is None

def test_baixar_estoque(db):
    repository = ProdutoRepository(db)

    produto = Produto(
        nome_produto="Produto Baixa Estoque",
        categoria="Teste",
        subcategoria="Estoque",
        preco_venda=Decimal("100.00"),
        preco_custo=Decimal("50.00"),
        quantidade_estoque=100,
    )

    produto_criado = repository.create(produto)

    resultado = repository.baixar_estoque(
        produto_criado.id_produto,
        10,
    )

    db.commit()

    assert resultado is True

    produto_atualizado = repository.get_by_id(
        produto_criado.id_produto
    )

    assert produto_atualizado is not None
    assert produto_atualizado.quantidade_estoque == 90


def test_baixar_estoque_insuficiente(db):
    repository = ProdutoRepository(db)

    produto = Produto(
        nome_produto="Produto Estoque Insuficiente",
        categoria="Teste",
        subcategoria="Estoque",
        preco_venda=Decimal("100.00"),
        preco_custo=Decimal("50.00"),
        quantidade_estoque=100,
    )

    produto_criado = repository.create(produto)

    resultado = repository.baixar_estoque(
        produto_criado.id_produto,
        101,
    )

    db.commit()

    assert resultado is False

    produto_atualizado = repository.get_by_id(
        produto_criado.id_produto
    )

    assert produto_atualizado is not None
    assert produto_atualizado.quantidade_estoque == 100

    def test_baixar_estoque_exatamente_disponivel(db):
        repository = ProdutoRepository(db)

        produto = Produto(
            nome_produto="Produto Estoque Exato",
            categoria="Teste",
            subcategoria="Estoque",
            preco_venda=Decimal("100.00"),
            preco_custo=Decimal("50.00"),
            quantidade_estoque=10,
        )

        produto_criado = repository.create(produto)

        resultado = repository.baixar_estoque(
            produto_criado.id_produto,
            10,
        )

        db.commit()

        assert resultado is True

        produto_atualizado = repository.get_by_id(
            produto_criado.id_produto
        )

        assert produto_atualizado is not None
        assert produto_atualizado.quantidade_estoque == 0

def test_baixar_estoque_produto_sem_estoque(db):
    repository = ProdutoRepository(db)

    produto = Produto(
        nome_produto="Produto Sem Estoque",
        categoria="Teste",
        subcategoria="Estoque",
        preco_venda=Decimal("100.00"),
        preco_custo=Decimal("50.00"),
        quantidade_estoque=0,
    )

    produto_criado = repository.create(produto)

    resultado = repository.baixar_estoque(
        produto_criado.id_produto,
        1,
    )

    db.commit()

    assert resultado is False

    produto_atualizado = repository.get_by_id(
        produto_criado.id_produto
    )

    assert produto_atualizado is not None
    assert produto_atualizado.quantidade_estoque == 0
