import math

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.api.exceptions.handlers import (
    ClienteAlreadyExistsException,
    ClienteNotFoundException,
)
from src.api.schemas.cliente_schemas import (
    ClienteCreate,
    ClienteUpdate,
)
from src.database.models.cliente import Cliente
from src.database.repositories.cliente_repository import ClienteRepository


class ClienteService:

    def __init__(self, db: Session):
        self.repository = ClienteRepository(db)
        self.db = db

    def criar(self, cliente_data: ClienteCreate) -> Cliente:
        cliente = Cliente(
            nome=cliente_data.nome,
            cpf_cnpj=cliente_data.cpf_cnpj,
            email=cliente_data.email,
            telefone=cliente_data.telefone,
            endereco=cliente_data.endereco,
            cidade=cliente_data.cidade,
            estado=cliente_data.estado,
            cep=cliente_data.cep,
        )

        try:
            return self.repository.create(cliente)

        except IntegrityError:
            self.db.rollback()

            raise ClienteAlreadyExistsException(
                "CPF/CNPJ ou e-mail já cadastrado."
            )

    def listar(self) -> list[Cliente]:
        return self.repository.get_all()

    def buscar_por_id(self, id_cliente: int) -> Cliente:
        cliente = self.repository.get_by_id(id_cliente)

        if cliente is None:
            raise ClienteNotFoundException(
                "Cliente não encontrado."
            )

        return cliente

    def atualizar(
        self,
        id_cliente: int,
        cliente_data: ClienteUpdate,
    ) -> Cliente:

        cliente = self.buscar_por_id(id_cliente)

        cliente.nome = cliente_data.nome
        cliente.cpf_cnpj = cliente_data.cpf_cnpj
        cliente.email = cliente_data.email
        cliente.telefone = cliente_data.telefone
        cliente.endereco = cliente_data.endereco
        cliente.cidade = cliente_data.cidade
        cliente.estado = cliente_data.estado
        cliente.cep = cliente_data.cep

        try:
            return self.repository.update(cliente)

        except IntegrityError:
            self.db.rollback()

            raise ClienteAlreadyExistsException(
                "CPF/CNPJ ou e-mail já cadastrado."
            )

    def excluir(self, id_cliente: int) -> None:
        cliente = self.buscar_por_id(id_cliente)

        self.repository.delete(cliente)

    def listar_paginado(
        self,
        page: int,
        limit: int,
    ):
        clientes, total = self.repository.get_paginated(
            page,
            limit,
        )

        pages = math.ceil(total / limit) if total > 0 else 0

        return {
            "items": clientes,
            "page": page,
            "limit": limit,
            "total": total,
            "pages": pages,
        }