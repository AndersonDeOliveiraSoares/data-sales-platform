from fastapi import FastAPI
from src.api.routes.produto_routes import router as produto_router


from src.api.exceptions.handlers import (
    ClienteAlreadyExistsException,
    ClienteNotFoundException,
    cliente_already_exists_handler,
    cliente_not_found_handler, ProdutoNotFoundException, produto_not_found_handler,
)
from src.api.routes.cliente_routes import router as cliente_router


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

app.include_router(cliente_router)
app.include_router(produto_router)