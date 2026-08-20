from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from src.database.connection import Base


class ItemPedido(Base):
    __tablename__ = "item_pedido"

    id_item_pedido: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    id_pedido: Mapped[int] = mapped_column(
        ForeignKey("pedido.id_pedido"),
        nullable=False,
    )

    id_produto: Mapped[int] = mapped_column(
        ForeignKey("produto.id_produto"),
        nullable=False,
    )

    quantidade: Mapped[int] = mapped_column(
        nullable=False,
    )

    preco_unitario: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    subtotal: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )