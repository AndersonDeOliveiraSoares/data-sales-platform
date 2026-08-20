from sqlalchemy import func, select, update
from sqlalchemy.orm import Session

from src.database.models.produto import Produto


class ProdutoRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        produto: Produto,
    ) -> Produto:

        self.db.add(produto)
        self.db.commit()
        self.db.refresh(produto)

        return produto

    def get_by_id(
        self,
        id_produto: int,
    ) -> Produto | None:

        statement = select(Produto).where(
            Produto.id_produto == id_produto
        )

        return self.db.scalar(statement)

    def get_all(self) -> list[Produto]:

        statement = (
            select(Produto)
            .order_by(Produto.id_produto)
        )

        return list(
            self.db.scalars(statement).all()
        )

    def get_paginated(
        self,
        page: int,
        limit: int,
    ) -> tuple[list[Produto], int]:

        offset = (page - 1) * limit

        statement = (
            select(Produto)
            .order_by(Produto.id_produto)
            .offset(offset)
            .limit(limit)
        )

        produtos = list(
            self.db.scalars(statement).all()
        )

        total_statement = (
            select(func.count())
            .select_from(Produto)
        )

        total = (
            self.db.scalar(total_statement)
            or 0
        )

        return produtos, total

    def baixar_estoque(
        self,
        id_produto: int,
        quantidade: int,
    ) -> bool:

        statement = (
            update(Produto)
            .where(
                Produto.id_produto == id_produto,
                Produto.quantidade_estoque >= quantidade,
            )
            .values(
                quantidade_estoque=(
                    Produto.quantidade_estoque
                    - quantidade
                )
            )
        )

        resultado = self.db.execute(statement)

        return resultado.rowcount == 1

    def update(
        self,
        produto: Produto,
    ) -> Produto:

        self.db.commit()
        self.db.refresh(produto)

        return produto

    def delete(
        self,
        produto: Produto,
    ) -> None:

        self.db.delete(produto)
        self.db.commit()