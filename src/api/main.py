from fastapi import FastAPI

from src.api.exceptions.handlers import (
    ClienteAlreadyExistsException,
    ClienteNotFoundException,
    cliente_already_exists_handler,
    cliente_not_found_handler,
    PedidoNotFoundException,
    pedido_not_found_handler,
    ProdutoNotFoundException,
    produto_not_found_handler,
    ItemPedidoNotFoundException,
    item_pedido_not_found_handler,
    EstoqueInsuficienteException,
    estoque_insuficiente_handler,
)
from src.api.routes.item_pedido_routes import router as item_pedido_router
from src.api.routes.cliente_routes import router as cliente_router
from src.api.routes.pedido_routes import router as pedido_router
from src.api.routes.produto_routes import router as produto_router


app = FastAPI(
    title="Data Sales Platform",
    version="0.1.0",
)


app.add_exception_handler(
    ClienteAlreadyExistsException,
    cliente_already_exists_handler,
)

app.add_exception_handler(
    ClienteNotFoundException,
    cliente_not_found_handler,
)

app.add_exception_handler(
    ProdutoNotFoundException,
    produto_not_found_handler,
)

app.add_exception_handler(
    PedidoNotFoundException,
    pedido_not_found_handler,
)

app.add_exception_handler(
    ItemPedidoNotFoundException,
    item_pedido_not_found_handler,
)

app.add_exception_handler(
    EstoqueInsuficienteException,
    estoque_insuficiente_handler,
)

app.include_router(cliente_router)
app.include_router(produto_router)
app.include_router(pedido_router)
app.include_router(item_pedido_router)