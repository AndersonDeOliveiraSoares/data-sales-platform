import pandas as pd
import pytest

from src.quality.parquet_quality import (
    validate_duplicates,
    validate_non_negative,
    validate_not_null,
    validate_positive,
    validate_required_columns,
)

def test_validate_required_columns_cliente():
    df = pd.DataFrame(
        {
            "id_cliente": [1],
            "nome": ["Anderson"],
            "cpf_cnpj": ["123"],
            "email": ["anderson@email.com"],
        }
    )

    validate_required_columns(
        df,
        "cliente",
    )


def test_validate_required_columns_detecta_coluna_ausente():
    df = pd.DataFrame(
        {
            "id_cliente": [1],
            "nome": ["Anderson"],
            "email": ["anderson@email.com"],
        }
    )

    with pytest.raises(ValueError):
        validate_required_columns(
            df,
            "cliente",
        )


def test_validate_not_null():
    df = pd.DataFrame(
        {
            "id_cliente": [1],
            "nome": ["Anderson"],
            "cpf_cnpj": ["123"],
            "email": ["anderson@email.com"],
        }
    )

    validate_not_null(
        df,
        "cliente",
    )


def test_validate_not_null_detecta_nulo():
    df = pd.DataFrame(
        {
            "id_cliente": [1],
            "nome": [None],
            "cpf_cnpj": ["123"],
            "email": ["anderson@email.com"],
        }
    )

    with pytest.raises(ValueError):
        validate_not_null(
            df,
            "cliente",
        )

def test_validate_non_negative():
    df = pd.DataFrame(
        {
            "preco_venda": [100.00, 200.00],
            "preco_custo": [50.00, 100.00],
        }
    )

    validate_non_negative(
        df,
        "produto",
        ["preco_venda", "preco_custo"],
    )


def test_validate_non_negative_detecta_negativo():
    df = pd.DataFrame(
        {
            "preco_venda": [100.00, -200.00],
            "preco_custo": [50.00, 100.00],
        }
    )

    with pytest.raises(ValueError):
        validate_non_negative(
            df,
            "produto",
            ["preco_venda", "preco_custo"],
        )


def test_validate_positive():
    df = pd.DataFrame(
        {
            "quantidade": [1, 2, 5],
        }
    )

    validate_positive(
        df,
        "item_pedido",
        ["quantidade"],
    )


def test_validate_positive_detecta_zero():
    df = pd.DataFrame(
        {
            "quantidade": [1, 0, 5],
        }
    )

    with pytest.raises(ValueError):
        validate_positive(
            df,
            "item_pedido",
            ["quantidade"],
        )

def test_validate_duplicates():
    df = pd.DataFrame(
        {
            "id_cliente": [1, 2],
            "cpf_cnpj": ["123", "456"],
            "email": [
                "anderson@email.com",
                "maria@email.com",
            ],
        }
    )

    validate_duplicates(
        df,
        "cliente",
        [
            "id_cliente",
            "cpf_cnpj",
            "email",
        ],
    )


def test_validate_duplicates_detecta_duplicado():
    df = pd.DataFrame(
        {
            "id_cliente": [1, 2],
            "cpf_cnpj": ["123", "123"],
            "email": [
                "anderson@email.com",
                "maria@email.com",
            ],
        }
    )

    with pytest.raises(ValueError):
        validate_duplicates(
            df,
            "cliente",
            [
                "id_cliente",
                "cpf_cnpj",
                "email",
            ],
        )