from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database.models.pedido import Pedido


class PedidoRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, pedido: Pedido) -> Pedido:
        self.db.add(pedido)
        self.db.commit()
        self.db.refresh(pedido)

        return pedido

    def get_by_id(self, id_pedido: int) -> Pedido | None:
        statement = select(Pedido).where(
            Pedido.id_pedido == id_pedido
        )

        return self.db.scalar(statement)

    def get_all(self) -> list[Pedido]:
        statement = select(Pedido)

        return list(self.db.scalars(statement).all())

    def delete(self, pedido: Pedido) -> None:
        self.db.delete(pedido)
        self.db.commit()