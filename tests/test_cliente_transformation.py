import pandas as pd

from src.transformation.cliente_transformation import (
transform_cliente,
)

def test_transform_cliente():
    df = pd.DataFrame(
        {
            "id_cliente": [1],
            "nome": ["  Anderson Tecnologia  "],
            "cpf_cnpj": ["10000000001"],
            "email": ["anderson@exemplo.com"],
            "telefone": ["21999990001"],
            "endereco": ["Rua das Flores, 100"],
            "cidade": ["Rio de Janeiro"],
            "estado": ["RJ"],
            "cep": ["23000001"],
        }
    )

    result = transform_cliente(df)

    assert len(result) == 1
    assert result["nome"].iloc[0] == "Anderson Tecnologia"

def test_transform_cliente_remove_espacos():

    df = pd.DataFrame(
        {
            "id_cliente": [1],
            "nome": ["  Anderson  "],
            "cpf_cnpj": ["10000000001"],
            "email": ["  anderson@exemplo.com  "],
            "telefone": ["21999990001"],
            "endereco": [" Rua das Flores, 100 "],
            "cidade": [" Rio de Janeiro "],
            "estado": [" RJ "],
            "cep": ["23000001"],
        }
    )

    result = transform_cliente(df)

    assert result["nome"].iloc[0] == "Anderson"
    assert result["email"].iloc[0] == "anderson@exemplo.com"
    assert result["endereco"].iloc[0] == "Rua das Flores, 100"
    assert result["cidade"].iloc[0] == "Rio de Janeiro"
    assert result["estado"].iloc[0] == "RJ"

