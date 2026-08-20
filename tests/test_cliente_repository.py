from src.database.models.cliente import Cliente
from src.database.repositories.cliente_repository import ClienteRepository


def test_create_cliente(db):
    repository = ClienteRepository(db)

    cliente = Cliente(
        nome="Cliente Repository Teste",
        cpf_cnpj="99999999999",
        email="repository@example.com",
    )

    resultado = repository.create(cliente)

    assert resultado.id_cliente is not None
    assert resultado.nome == "Cliente Repository Teste"
    assert resultado.cpf_cnpj == "99999999999"
    assert resultado.email == "repository@example.com"


def test_get_by_id(db):
    repository = ClienteRepository(db)

    cliente = Cliente(
        nome="Cliente Busca",
        cpf_cnpj="88888888888",
        email="busca@example.com",
    )

    cliente_criado = repository.create(cliente)

    resultado = repository.get_by_id(cliente_criado.id_cliente)

    assert resultado is not None
    assert resultado.id_cliente == cliente_criado.id_cliente
    assert resultado.nome == "Cliente Busca"


def test_get_all(db):
    repository = ClienteRepository(db)

    cliente1 = Cliente(
        nome="Cliente Lista 1",
        cpf_cnpj="77777777777",
        email="lista1@example.com",
    )

    cliente2 = Cliente(
        nome="Cliente Lista 2",
        cpf_cnpj="66666666666",
        email="lista2@example.com",
    )

    repository.create(cliente1)
    repository.create(cliente2)

    resultado = repository.get_all()

    assert len(resultado) >= 2
    assert any(cliente.nome == "Cliente Lista 1" for cliente in resultado)
    assert any(cliente.nome == "Cliente Lista 2" for cliente in resultado)


def test_delete(db):
    repository = ClienteRepository(db)

    cliente = Cliente(
        nome="Cliente Excluir",
        cpf_cnpj="55555555555",
        email="excluir@example.com",
    )

    cliente_criado = repository.create(cliente)

    repository.delete(cliente_criado)

    resultado = repository.get_by_id(cliente_criado.id_cliente)

    assert resultado is None