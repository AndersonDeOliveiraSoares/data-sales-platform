from decimal import Decimal

from sqlalchemy import Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from src.database.connection import Base


class Produto(Base):
    __tablename__ = "produto"

    id_produto: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    nome_produto: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    categoria: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    subcategoria: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    preco_venda: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    preco_custo: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    quantidade_estoque: Mapped[int] = mapped_column(
        nullable=False,
        default=0,
    )