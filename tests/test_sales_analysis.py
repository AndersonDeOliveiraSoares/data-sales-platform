import pandas as pd
import pytest

from src.analytics.sales_analysis import calculate_sales_indicators


@pytest.fixture
def dados_fact_vendas():
    return pd.DataFrame(
        {
            "id_pedido": [1, 1, 2],
            "quantidade": [2, 1, 3],
            "receita": [200.00, 50.00, 300.00],
            "custo_total": [120.00, 30.00, 180.00],
            "lucro": [80.00, 20.00, 120.00],
        }
    )


def test_calculate_sales_indicators_receita_total(
    dados_fact_vendas,
):
    indicadores = calculate_sales_indicators(
        dados_fact_vendas
    )

    assert indicadores["receita_total"] == 550.00


def test_calculate_sales_indicators_custo_total(
    dados_fact_vendas,
):
    indicadores = calculate_sales_indicators(
        dados_fact_vendas
    )

    assert indicadores["custo_total"] == 330.00


def test_calculate_sales_indicators_lucro_total(
    dados_fact_vendas,
):
    indicadores = calculate_sales_indicators(
        dados_fact_vendas
    )

    assert indicadores["lucro_total"] == 220.00


def test_calculate_sales_indicators_quantidade_vendida(
    dados_fact_vendas,
):
    indicadores = calculate_sales_indicators(
        dados_fact_vendas
    )

    assert indicadores["quantidade_vendida"] == 6


def test_calculate_sales_indicators_margem(
    dados_fact_vendas,
):
    indicadores = calculate_sales_indicators(
        dados_fact_vendas
    )

    assert indicadores["margem"] == pytest.approx(
        220 / 550
    )


def test_calculate_sales_indicators_ticket_medio(
    dados_fact_vendas,
):
    indicadores = calculate_sales_indicators(
        dados_fact_vendas
    )

    assert indicadores["ticket_medio"] == pytest.approx(
        550 / 2
    )


def test_calculate_sales_indicators_quantidade_pedidos_distintos(
    dados_fact_vendas,
):
    indicadores = calculate_sales_indicators(
        dados_fact_vendas
    )

    assert indicadores["ticket_medio"] == pytest.approx(
        275.00
    )


def test_calculate_sales_indicators_receita_zero():
    fact_vendas = pd.DataFrame(
        {
            "id_pedido": [1],
            "quantidade": [1],
            "receita": [0.00],
            "custo_total": [0.00],
            "lucro": [0.00],
        }
    )

    indicadores = calculate_sales_indicators(
        fact_vendas
    )

    assert indicadores["margem"] == 0
    assert indicadores["ticket_medio"] == 0