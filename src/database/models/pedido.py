from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from src.database.connection import Base


class Pedido(Base):
    __tablename__ = "pedido"

    id_pedido: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    id_cliente: Mapped[int] = mapped_column(
        ForeignKey("cliente.id_cliente"),
        nullable=False,
    )

    data_pedido: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        nullable=False,
    )

    status_pedido: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="PENDENTE",
    )

    valor_total: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    valor_frete: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
        default=Decimal("0.00"),
    )

    forma_pagamento: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

