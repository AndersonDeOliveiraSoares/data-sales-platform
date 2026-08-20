from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from src.api.schemas.pedido_schemas import (
    PedidoCreate,
    PedidoListResponse,
    PedidoResponse,
    PedidoUpdate,
)
from src.database.connection import get_db
from src.services.pedido_service import PedidoService


router = APIRouter(
    prefix="/pedidos",
    tags=["Pedidos"],
)


@router.post(
    "/",
    response_model=PedidoResponse,
    status_code=status.HTTP_201_CREATED,
)
def criar_pedido(
    pedido_data: PedidoCreate,
    db: Session = Depends(get_db),
):
    service = PedidoService(db)

    return service.criar(pedido_data)


@router.get(
    "/",
    response_model=PedidoListResponse,
)
def listar_pedidos(
    page: int = Query(
        1,
        ge=1,
        description="Número da página",
    ),
    limit: int = Query(
        10,
        ge=1,
        le=100,
        description="Quantidade de pedidos por página",
    ),
    db: Session = Depends(get_db),
):
    service = PedidoService(db)

    return service.listar_paginado(
        page=page,
        limit=limit,
    )


@router.get(
    "/{id_pedido}",
    response_model=PedidoResponse,
)
def buscar_pedido(
    id_pedido: int,
    db: Session = Depends(get_db),
):
    service = PedidoService(db)

    return service.buscar_por_id(id_pedido)


@router.put(
    "/{id_pedido}",
    response_model=PedidoResponse,
)
def atualizar_pedido(
    id_pedido: int,
    pedido_data: PedidoUpdate,
    db: Session = Depends(get_db),
):
    service = PedidoService(db)

    return service.atualizar(
        id_pedido=id_pedido,
        pedido_data=pedido_data,
    )


@router.delete(
    "/{id_pedido}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def excluir_pedido(
    id_pedido: int,
    db: Session = Depends(get_db),
):
    service = PedidoService(db)

    service.excluir(id_pedido)
