from sqlalchemy import func, select
from sqlalchemy.orm import Session

from src.database.models.item_pedido import ItemPedido


class ItemPedidoRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, item: ItemPedido) -> ItemPedido:
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)

        return item

    def get_by_id(
        self,
        id_item_pedido: int,
    ) -> ItemPedido | None:

        statement = select(ItemPedido).where(
            ItemPedido.id_item_pedido == id_item_pedido
        )

        return self.db.scalar(statement)

    def get_all(self) -> list[ItemPedido]:
        statement = (
            select(ItemPedido)
            .order_by(ItemPedido.id_item_pedido)
        )

        return list(
            self.db.scalars(statement).all()
        )

    def get_by_pedido(
        self,
        id_pedido: int,
    ) -> list[ItemPedido]:

        statement = (
            select(ItemPedido)
            .where(ItemPedido.id_pedido == id_pedido)
            .order_by(ItemPedido.id_item_pedido)
        )

        return list(
            self.db.scalars(statement).all()
        )

    def get_paginated(
        self,
        page: int,
        limit: int,
    ) -> tuple[list[ItemPedido], int]:

        offset = (page - 1) * limit

        statement = (
            select(ItemPedido)
            .order_by(ItemPedido.id_item_pedido)
            .offset(offset)
            .limit(limit)
        )

        items = list(
            self.db.scalars(statement).all()
        )

        total_statement = (
            select(func.count())
            .select_from(ItemPedido)
        )

        total = self.db.scalar(total_statement) or 0

        return items, total

    def update(
        self,
        item: ItemPedido,
    ) -> ItemPedido:

        self.db.commit()
        self.db.refresh(item)

        return item

    def delete(self, item: ItemPedido) -> None:
        self.db.delete(item)
        self.db.commit()