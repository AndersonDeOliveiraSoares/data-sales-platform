from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from src.api.schemas.cliente_schemas import (
    ClienteCreate,
    ClienteListResponse,
    ClienteResponse,
    ClienteUpdate,
)
from src.database.connection import get_db
from src.services.cliente_service import ClienteService


router = APIRouter(
    prefix="/clientes",
    tags=["Clientes"],
)


@router.post(
    "/",
    response_model=ClienteResponse,
    status_code=status.HTTP_201_CREATED,
)
def criar_cliente(
    cliente_data: ClienteCreate,
    db: Session = Depends(get_db),
):
    service = ClienteService(db)

    return service.criar(cliente_data)


@router.get(
    "/",
    response_model=ClienteListResponse,
)
def listar_clientes(
    page: int = Query(
        1,
        ge=1,
        description="Número da página",
    ),
    limit: int = Query(
        10,
        ge=1,
        le=100,
        description="Quantidade de clientes por página",
    ),
    db: Session = Depends(get_db),
):
    service = ClienteService(db)

    return service.listar_paginado(
        page=page,
        limit=limit,
    )


@router.get(
    "/{id_cliente}",
    response_model=ClienteResponse,
)
def buscar_cliente(
    id_cliente: int,
    db: Session = Depends(get_db),
):
    service = ClienteService(db)

    return service.buscar_por_id(id_cliente)


@router.put(
    "/{id_cliente}",
    response_model=ClienteResponse,
)
def atualizar_cliente(
    id_cliente: int,
    cliente_data: ClienteUpdate,
    db: Session = Depends(get_db),
):
    service = ClienteService(db)

    return service.atualizar(
        id_cliente=id_cliente,
        cliente_data=cliente_data,
    )


@router.delete(
    "/{id_cliente}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def excluir_cliente(
    id_cliente: int,
    db: Session = Depends(get_db),
):
    service = ClienteService(db)

    service.excluir(id_cliente)