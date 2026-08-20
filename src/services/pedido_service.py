import math
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.api.exceptions.handlers import (
    ClienteNotFoundException,
    EstoqueInsuficienteException,
    PedidoNotFoundException,
    ProdutoNotFoundException,
)
from src.api.schemas.pedido_schemas import (
    PedidoCreate,
    PedidoUpdate,
)
from src.database.models.item_pedido import ItemPedido
from src.database.models.pedido import Pedido
from src.database.repositories.cliente_repository import (
    ClienteRepository,
)
from src.database.repositories.pedido_repository import (
    PedidoRepository,
)
from src.database.repositories.produto_repository import (
    ProdutoRepository,
)


class PedidoService:

    def __init__(self, db: Session):
        self.db = db

        self.repository = PedidoRepository(db)

        self.cliente_repository = ClienteRepository(db)

        self.produto_repository = ProdutoRepository(db)

    def criar(
        self,
        pedido_data: PedidoCreate,
    ) -> Pedido:

        cliente = self.cliente_repository.get_by_id(
            pedido_data.id_cliente
        )

        if cliente is None:
            raise ClienteNotFoundException(
                "Cliente não encontrado."
            )

        try:
            pedido = Pedido(
                id_cliente=pedido_data.id_cliente,
                valor_total=0,
                valor_frete=pedido_data.valor_frete,
                forma_pagamento=pedido_data.forma_pagamento,
            )

            self.db.add(pedido)

            # Gera o ID do pedido antes de criar os itens.
            self.db.flush()

            valor_total = 0

            produtos = []

            # ==========================================
            # 1. VALIDAR TODOS OS PRODUTOS E ESTOQUE
            # ==========================================

            for item_data in pedido_data.itens:

                produto = self.produto_repository.get_by_id(
                    item_data.id_produto
                )

                if produto is None:
                    raise ProdutoNotFoundException(
                        "Produto não encontrado."
                    )

                if (
                    produto.quantidade_estoque
                    < item_data.quantidade
                ):
                    raise EstoqueInsuficienteException(
                        f"Estoque insuficiente para o produto "
                        f"'{produto.nome_produto}'. "
                        f"Disponível: "
                        f"{produto.quantidade_estoque}. "
                        f"Solicitado: "
                        f"{item_data.quantidade}."
                    )

                preco_unitario = produto.preco_venda

                subtotal = (
                    preco_unitario
                    * item_data.quantidade
                )

                produtos.append(
                    (
                        item_data,
                        produto,
                        preco_unitario,
                        subtotal,
                    )
                )

                valor_total += subtotal

            # ==========================================
            # 2. CRIAR ITENS E BAIXAR ESTOQUE
            # ==========================================

            for (
                item_data,
                produto,
                preco_unitario,
                subtotal,
            ) in produtos:

                estoque_baixado = (
                    self.produto_repository.baixar_estoque(
                        produto.id_produto,
                        item_data.quantidade,
                    )
                )

                if not estoque_baixado:
                    raise EstoqueInsuficienteException(
                        f"Estoque insuficiente para o produto "
                        f"'{produto.nome_produto}'. "
                        f"Disponível: "
                        f"{produto.quantidade_estoque}. "
                        f"Solicitado: "
                        f"{item_data.quantidade}."
                    )

                item = ItemPedido(
                    id_pedido=pedido.id_pedido,
                    id_produto=produto.id_produto,
                    quantidade=item_data.quantidade,
                    preco_unitario=preco_unitario,
                    subtotal=subtotal,
                )

                self.db.add(item)

            # ==========================================
            # 3. CALCULAR TOTAL DO PEDIDO
            # ==========================================

            pedido.valor_total = (
                valor_total
                + pedido_data.valor_frete
            )

            # ==========================================
            # 4. COMMIT ÚNICO
            # ==========================================

            self.db.commit()

            self.db.refresh(pedido)

            return pedido

        except Exception:
            # Qualquer erro desfaz toda a transação:
            #
            # - Pedido
            # - ItemPedido
            # - Baixa de estoque
            #
            self.db.rollback()

            raise

    def listar(self) -> list[Pedido]:
        return self.repository.get_all()

    def buscar_por_id(
        self,
        id_pedido: int,
    ) -> Pedido:

        pedido = self.repository.get_by_id(
            id_pedido
        )

        if pedido is None:
            raise PedidoNotFoundException(
                "Pedido não encontrado."
            )

        return pedido

    def atualizar(
            self,
            id_pedido: int,
            pedido_data: PedidoUpdate,
    ) -> Pedido:

        pedido = self.buscar_por_id(
            id_pedido
        )

        pedido.status_pedido = (
            pedido_data.status_pedido
        )

        pedido.valor_frete = (
            pedido_data.valor_frete
        )

        pedido.forma_pagamento = (
            pedido_data.forma_pagamento
        )

        statement = select(ItemPedido).where(
            ItemPedido.id_pedido == id_pedido
        )

        itens = list(
            self.db.scalars(statement).all()
        )

        valor_itens = sum(
            (
                item.subtotal
                for item in itens
            ),
            0,
        )

        pedido.valor_total = (
                valor_itens
                + pedido_data.valor_frete
        )

        return self.repository.update(
            pedido
        )

    def excluir(
        self,
        id_pedido: int,
    ) -> None:

        pedido = self.buscar_por_id(
            id_pedido
        )

        self.repository.delete(pedido)

    def listar_paginado(
        self,
        page: int,
        limit: int,
    ):
        pedidos, total = (
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
            "items": pedidos,
            "page": page,
            "limit": limit,
            "total": total,
            "pages": pages,
        }