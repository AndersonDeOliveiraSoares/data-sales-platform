from src.database.models.cliente import Cliente


def test_cliente_model():
    cliente = Cliente(
        nome="Cliente Teste",
        cpf_cnpj="12345678900",
        email="teste@example.com",
    )

    assert cliente.nome == "Cliente Teste"
    assert cliente.cpf_cnpj == "12345678900"
    assert cliente.email == "teste@example.com"