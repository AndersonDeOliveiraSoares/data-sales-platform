from fastapi import Request
from fastapi.responses import JSONResponse


class AppException(Exception):
    """Exceção base da aplicação."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class ClienteNotFoundException(AppException):
    """Cliente não encontrado."""


class ClienteAlreadyExistsException(AppException):
    """Cliente já cadastrado."""


class ProdutoNotFoundException(AppException):
    """Produto não encontrado."""

class PedidoNotFoundException(AppException):
    """Pedido não encontrado."""

class ItemPedidoNotFoundException(AppException):
    """Item do pedido não encontrado."""

class EstoqueInsuficienteException(AppException):
    """Estoque insuficiente para realizar a venda."""

async def cliente_not_found_handler(
    request: Request,
    exc: ClienteNotFoundException,
):
    return JSONResponse(
        status_code=404,
        content={
            "detail": exc.message,
        },
    )


async def cliente_already_exists_handler(
    request: Request,
    exc: ClienteAlreadyExistsException,
):
    return JSONResponse(
        status_code=409,
        content={
            "detail": exc.message,
        },
    )


async def produto_not_found_handler(
    request: Request,
    exc: ProdutoNotFoundException,
):
    return JSONResponse(
        status_code=404,
        content={
            "detail": exc.message,
        },
    )

async def pedido_not_found_handler(
    request: Request,
    exc: PedidoNotFoundException,
):
    return JSONResponse(
        status_code=404,
        content={
            "detail": exc.message,
        },
    )

async def item_pedido_not_found_handler(
    request: Request,
    exc: ItemPedidoNotFoundException,
):
    return JSONResponse(
        status_code=404,
        content={
            "detail": exc.message,
        },
    )

async def estoque_insuficiente_handler(
    request: Request,
    exc: EstoqueInsuficienteException,
):
    return JSONResponse(
        status_code=400,
        content={
            "detail": exc.message,
        },
    )