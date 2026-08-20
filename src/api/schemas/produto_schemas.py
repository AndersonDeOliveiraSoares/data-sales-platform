from decimal import Decimal

from pydantic import BaseModel, Field


class ProdutoCreate(BaseModel):
    nome_produto: str
    categoria: str
    subcategoria: str | None = None

    preco_venda: Decimal = Field(
        ...,
        max_digits=12,
        decimal_places=2,
        description="Preço de venda do produto",
    )

    preco_custo: Decimal = Field(
        ...,
        max_digits=12,
        decimal_places=2,
        description="Preço de custo do produto",
    )

    quantidade_estoque: int


class ProdutoUpdate(BaseModel):
    nome_produto: str
    categoria: str
    subcategoria: str | None = None

    preco_venda: Decimal = Field(
        ...,
        max_digits=12,
        decimal_places=2,
        description="Preço de venda do produto",
    )

    preco_custo: Decimal = Field(
        ...,
        max_digits=12,
        decimal_places=2,
        description="Preço de custo do produto",
    )

    quantidade_estoque: int


class ProdutoResponse(BaseModel):
    id_produto: int
    nome_produto: str
    categoria: str
    subcategoria: str | None
    preco_venda: Decimal
    preco_custo: Decimal
    quantidade_estoque: int

    model_config = {
        "from_attributes": True
    }


class ProdutoListResponse(BaseModel):
    items: list[ProdutoResponse]
    page: int
    limit: int
    total: int
    pages: int