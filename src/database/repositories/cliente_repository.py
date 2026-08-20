from sqlalchemy import func, select
from sqlalchemy.orm import Session

from src.database.models.cliente import Cliente


class ClienteRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, cliente: Cliente) -> Cliente:
        self.db.add(cliente)
        self.db.commit()
        self.db.refresh(cliente)

        return cliente

    def get_by_id(self, id_cliente: int) -> Cliente | None:
        statement = select(Cliente).where(
            Cliente.id_cliente == id_cliente
        )

        return self.db.scalar(statement)

    def get_all(self) -> list[Cliente]:
        statement = select(Cliente)

        return list(
            self.db.scalars(statement).all()
        )

    def get_paginated(
        self,
        page: int,
        limit: int,
    ) -> tuple[list[Cliente], int]:

        offset = (page - 1) * limit

        statement = (
            select(Cliente)
            .order_by(Cliente.id_cliente)
            .offset(offset)
            .limit(limit)
        )

        clientes = list(
            self.db.scalars(statement).all()
        )

        total_statement = select(
            func.count()
        ).select_from(Cliente)

        total = self.db.scalar(total_statement) or 0

        return clientes, total

    def update(self, cliente: Cliente) -> Cliente:
        self.db.commit()
        self.db.refresh(cliente)

        return cliente

    def delete(self, cliente: Cliente) -> None:
        self.db.delete(cliente)
        self.db.commit()