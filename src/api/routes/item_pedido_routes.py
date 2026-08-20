from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from src.api.schemas.item_pedido_schemas import (
    ItemPedidoCreate,
    ItemPedidoListResponse,
    ItemPedidoResponse,
    ItemPedidoUpdate,
)
from src.database.connection import get_db
from src.services.item_pedido_service import ItemPedidoService


router = APIRouter(
    prefix="/itens-pedido",
    tags=["Itens do Pedido"],
)


@router.post(
    "/",
    response_model=ItemPedidoResponse,
    status_code=status.HTTP_201_CREATED,
)
def criar_item_pedido(
    item_data: ItemPedidoCreate,
    db: Session = Depends(get_db),
):
    service = ItemPedidoService(db)

    return service.criar(item_data)


@router.get(
    "/",
    response_model=ItemPedidoListResponse,
)
def listar_itens_pedido(
    page: int = Query(
        1,
        ge=1,
        description="Número da página",
    ),
    limit: int = Query(
        10,
        ge=1,
        le=100,
        description="Quantidade de itens por página",
    ),
    db: Session = Depends(get_db),
):
    service = ItemPedidoService(db)

    return service.listar_paginado(
        page=page,
        limit=limit,
    )


@router.get(
    "/pedido/{id_pedido}",
    response_model=list[ItemPedidoResponse],
)
def listar_itens_por_pedido(
    id_pedido: int,
    db: Session = Depends(get_db),
):
    service = ItemPedidoService(db)

    return service.listar_por_pedido(id_pedido)


@router.get(
    "/{id_item_pedido}",
    response_model=ItemPedidoResponse,
)
def buscar_item_pedido(
    id_item_pedido: int,
    db: Session = Depends(get_db),
):
    service = ItemPedidoService(db)

    return service.buscar_por_id(id_item_pedido)


@router.put(
    "/{id_item_pedido}",
    response_model=ItemPedidoResponse,
)
def atualizar_item_pedido(
    id_item_pedido: int,
    item_data: ItemPedidoUpdate,
    db: Session = Depends(get_db),
):
    service = ItemPedidoService(db)

    return service.atualizar(
        id_item_pedido=id_item_pedido,
        item_data=item_data,
    )


@router.delete(
    "/{id_item_pedido}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def excluir_item_pedido(
    id_item_pedido: int,
    db: Session = Depends(get_db),
):
    service = ItemPedidoService(db)

    service.excluir(id_item_pedido)