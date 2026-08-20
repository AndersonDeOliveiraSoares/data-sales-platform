import math

from sqlalchemy.orm import Session

from src.api.exceptions.handlers import (
    ItemPedidoNotFoundException,
    PedidoNotFoundException,
    ProdutoNotFoundException,
)
from src.api.schemas.item_pedido_schemas import (
    ItemPedidoCreate,
    ItemPedidoUpdate,
)
from src.database.models.item_pedido import ItemPedido
from src.database.repositories.item_pedido_repository import (
    ItemPedidoRepository,
)
from src.database.repositories.pedido_repository import (
    PedidoRepository,
)
from src.database.repositories.produto_repository import (
    ProdutoRepository,
)


class ItemPedidoService:

    def __init__(self, db: Session):
        self.repository = ItemPedidoRepository(db)

        self.pedido_repository = PedidoRepository(db)

        self.produto_repository = ProdutoRepository(db)

    def criar(
        self,
        item_data: ItemPedidoCreate,
    ) -> ItemPedido:

        pedido = self.pedido_repository.get_by_id(
            item_data.id_pedido
        )

        if pedido is None:
            raise PedidoNotFoundException(
                "Pedido não encontrado."
            )

        produto = self.produto_repository.get_by_id(
            item_data.id_produto
        )

        if produto is None:
            raise ProdutoNotFoundException(
                "Produto não encontrado."
            )

        preco_unitario = produto.preco_venda

        subtotal = (
            preco_unitario
            * item_data.quantidade
        )

        item = ItemPedido(
            id_pedido=item_data.id_pedido,
            id_produto=item_data.id_produto,
            quantidade=item_data.quantidade,
            preco_unitario=preco_unitario,
            subtotal=subtotal,
        )

        return self.repository.create(item)

    def listar(self) -> list[ItemPedido]:
        return self.repository.get_all()

    def listar_paginado(
        self,
        page: int,
        limit: int,
    ):
        items, total = (
            self.repository.get_paginated(
                page,
                limit,
            )
        )

        pages = (
            math.ceil(total / limit)
            if total > 0
            else 0
        )

        return {
            "items": items,
            "page": page,
            "limit": limit,
            "total": total,
            "pages": pages,
        }

    def buscar_por_id(
        self,
        id_item_pedido: int,
    ) -> ItemPedido:

        item = self.repository.get_by_id(
            id_item_pedido
        )

        if item is None:
            raise ItemPedidoNotFoundException(
                "Item do pedido não encontrado."
            )

        return item

    def listar_por_pedido(
        self,
        id_pedido: int,
    ) -> list[ItemPedido]:

        pedido = self.pedido_repository.get_by_id(
            id_pedido
        )

        if pedido is None:
            raise PedidoNotFoundException(
                "Pedido não encontrado."
            )

        return self.repository.get_by_pedido(
            id_pedido
        )

    def atualizar(
        self,
        id_item_pedido: int,
        item_data: ItemPedidoUpdate,
    ) -> ItemPedido:

        item = self.buscar_por_id(
            id_item_pedido
        )

        produto = self.produto_repository.get_by_id(
            item.id_produto
        )

        if produto is None:
            raise ProdutoNotFoundException(
                "Produto não encontrado."
            )

        item.quantidade = (
            item_data.quantidade
        )

        item.preco_unitario = (
            produto.preco_venda
        )

        item.subtotal = (
            item.preco_unitario
            * item.quantidade
        )

        return self.repository.update(
            item
        )

    def excluir(
        self,
        id_item_pedido: int,
    ) -> None:

        item = self.buscar_por_id(
            id_item_pedido
        )

        self.repository.delete(item)