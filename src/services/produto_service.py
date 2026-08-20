import math

from sqlalchemy.orm import Session

from src.api.exceptions.handlers import ProdutoNotFoundException
from src.api.schemas.produto_schemas import ProdutoCreate, ProdutoUpdate
from src.database.models.produto import Produto
from src.database.repositories.produto_repository import ProdutoRepository


class ProdutoService:

    def __init__(self, db: Session):
        self.repository = ProdutoRepository(db)

    def criar(self, produto_data: ProdutoCreate) -> Produto:
        produto = Produto(
            nome_produto=produto_data.nome_produto,
            categoria=produto_data.categoria,
            subcategoria=produto_data.subcategoria,
            preco_venda=produto_data.preco_venda,
            preco_custo=produto_data.preco_custo,
            quantidade_estoque=produto_data.quantidade_estoque,
        )

        return self.repository.create(produto)

    def listar(self) -> list[Produto]:
        return self.repository.get_all()

    def buscar_por_id(self, id_produto: int) -> Produto:
        produto = self.repository.get_by_id(id_produto)

        if produto is None:
            raise ProdutoNotFoundException(
                "Produto não encontrado."
            )

        return produto

    def atualizar(
        self,
        id_produto: int,
        produto_data: ProdutoUpdate,
    ) -> Produto:
        produto = self.buscar_por_id(id_produto)

        produto.nome_produto = produto_data.nome_produto
        produto.categoria = produto_data.categoria
        produto.subcategoria = produto_data.subcategoria
        produto.preco_venda = produto_data.preco_venda
        produto.preco_custo = produto_data.preco_custo
        produto.quantidade_estoque = produto_data.quantidade_estoque

        return self.repository.update(produto)

    def excluir(self, id_produto: int) -> None:
        produto = self.buscar_por_id(id_produto)

        self.repository.delete(produto)

    def listar_paginado(
        self,
        page: int,
        limit: int,
    ):
        produtos, total = self.repository.get_paginated(
            page,
            limit,
        )

        pages = math.ceil(total / limit) if total > 0 else 0

        return {
            "items": produtos,
            "page": page,
            "limit": limit,
            "total": total,
            "pages": pages,
        }