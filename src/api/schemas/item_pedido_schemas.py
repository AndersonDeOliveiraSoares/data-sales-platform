from decimal import Decimal

from pydantic import BaseModel, Field


class ItemPedidoCreate(BaseModel):
    id_pedido: int = Field(
        ...,
        gt=0,
        description="ID do pedido",
    )

    id_produto: int = Field(
        ...,
        gt=0,
        description="ID do produto",
    )

    quantidade: int = Field(
        ...,
        gt=0,
        description="Quantidade do produto",
    )


class ItemPedidoUpdate(BaseModel):
    quantidade: int = Field(
        ...,
        gt=0,
        description="Quantidade do produto",
    )


class ItemPedidoResponse(BaseModel):
    id_item_pedido: int
    id_pedido: int
    id_produto: int
    quantidade: int
    preco_unitario: Decimal
    subtotal: Decimal

    model_config = {
        "from_attributes": True
    }


class ItemPedidoListResponse(BaseModel):
    items: list[ItemPedidoResponse]
    page: int
    limit: int
    total: int
    pages: int