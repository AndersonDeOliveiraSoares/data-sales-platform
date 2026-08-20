from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from src.api.schemas.produto_schemas import (
    ProdutoCreate,
    ProdutoListResponse,
    ProdutoResponse,
    ProdutoUpdate,
)
from src.database.connection import get_db
from src.services.produto_service import ProdutoService


router = APIRouter(
    prefix="/produtos",
    tags=["Produtos"],
)


@router.post(
    "/",
    response_model=ProdutoResponse,
    status_code=status.HTTP_201_CREATED,
)
def criar_produto(
    produto_data: ProdutoCreate,
    db: Session = Depends(get_db),
):
    service = ProdutoService(db)

    return service.criar(produto_data)


@router.get(
    "/",
    response_model=ProdutoListResponse,
)
def listar_produtos(
    page: int = Query(
        1,
        ge=1,
        description="Número da página",
    ),
    limit: int = Query(
        10,
        ge=1,
        le=100,
        description="Quantidade de produtos por página",
    ),
    db: Session = Depends(get_db),
):
    service = ProdutoService(db)

    return service.listar_paginado(
        page=page,
        limit=limit,
    )


@router.get(
    "/{id_produto}",
    response_model=ProdutoResponse,
)
def buscar_produto(
    id_produto: int,
    db: Session = Depends(get_db),
):
    service = ProdutoService(db)

    return service.buscar_por_id(id_produto)


@router.put(
    "/{id_produto}",
    response_model=ProdutoResponse,
)
def atualizar_produto(
    id_produto: int,
    produto_data: ProdutoUpdate,
    db: Session = Depends(get_db),
):
    service = ProdutoService(db)

    return service.atualizar(
        id_produto=id_produto,
        produto_data=produto_data,
    )


@router.delete(
    "/{id_produto}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def excluir_produto(
    id_produto: int,
    db: Session = Depends(get_db),
):
    service = ProdutoService(db)

    service.excluir(id_produto)