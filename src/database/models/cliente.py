from datetime import datetime

from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from src.database.connection import Base


class Cliente(Base):
    __tablename__ = "cliente"

    id_cliente: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    nome: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    cpf_cnpj: Mapped[str] = mapped_column(
        String(18),
        unique=True,
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        nullable=False,
    )

    telefone: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    endereco: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True,
    )

    cidade: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    estado: Mapped[str | None] = mapped_column(
        String(2),
        nullable=True,
    )

    cep: Mapped[str | None] = mapped_column(
        String(9),
        nullable=True,
    )

    data_cadastro: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        nullable=False,
    )