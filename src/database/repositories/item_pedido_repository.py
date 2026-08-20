from sqlalchemy import select
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

    def get_by_id(self, id_item_pedido: int) -> ItemPedido | None:
        statement = select(ItemPedido).where(
            ItemPedido.id_item_pedido == id_item_pedido
        )

        return self.db.scalar(statement)

    def get_all(self) -> list[ItemPedido]:
        statement = select(ItemPedido)

        return list(self.db.scalars(statement).all())

    def delete(self, item: ItemPedido) -> None:
        self.db.delete(item)
        self.db.commit()