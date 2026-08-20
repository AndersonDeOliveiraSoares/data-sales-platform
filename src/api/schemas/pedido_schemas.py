from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class PedidoItemCreate(BaseModel):
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


class PedidoCreate(BaseModel):
    id_cliente: int = Field(
        ...,
        gt=0,
        description="ID do cliente",
    )

    itens: list[PedidoItemCreate] = Field(
        ...,
        min_length=1,
        description="Itens do pedido",
    )

    valor_frete: Decimal = Field(
        default=Decimal("0.00"),
        ge=0,
        max_digits=12,
        decimal_places=2,
    )

    forma_pagamento: str = Field(
        ...,
        min_length=1,
        max_length=30,
    )


class PedidoUpdate(BaseModel):
    status_pedido: str = Field(
        ...,
        min_length=1,
        max_length=20,
    )

    valor_total: Decimal = Field(
        ...,
        ge=0,
        max_digits=12,
        decimal_places=2,
    )

    valor_frete: Decimal = Field(
        ...,
        ge=0,
        max_digits=12,
        decimal_places=2,
    )

    forma_pagamento: str = Field(
        ...,
        min_length=1,
        max_length=30,
    )


class PedidoResponse(BaseModel):
    id_pedido: int
    id_cliente: int
    data_pedido: datetime
    status_pedido: str
    valor_total: Decimal
    valor_frete: Decimal
    forma_pagamento: str

    model_config = {
        "from_attributes": True
    }


class PedidoListResponse(BaseModel):
    items: list[PedidoResponse]
    page: int
    limit: int
    total: int
    pages: int