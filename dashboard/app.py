import pandas as pd
import streamlit as st

from src.analytics.service import (
    get_available_years_service,
    get_sales_summary_service,
    get_sales_by_product_service,
    get_sales_by_customer_service,
    get_sales_by_month_service,
)


st.set_page_config(
    page_title="Data Sales Platform",
    page_icon="📊",
    layout="wide",
)


# ============================================================
# CONFIGURAÇÃO
# ============================================================

st.title("📊 Data Sales Platform")
st.subheader("Visão Geral de Vendas")


# ============================================================
# FILTROS
# ============================================================

anos = get_available_years_service()

if not anos:
    st.warning("Nenhum dado disponível no Data Warehouse.")
    st.stop()


col_filtro_ano, col_filtro_mes = st.columns(2)


with col_filtro_ano:
    ano_selecionado = st.selectbox(
        "Ano",
        options=anos,
    )


meses = {
    1: "Janeiro",
    2: "Fevereiro",
    3: "Março",
    4: "Abril",
    5: "Maio",
    6: "Junho",
    7: "Julho",
    8: "Agosto",
    9: "Setembro",
    10: "Outubro",
    11: "Novembro",
    12: "Dezembro",
}


with col_filtro_mes:
    mes_selecionado = st.selectbox(
        "Mês",
        options=[None] + list(meses.keys()),
        format_func=lambda mes: (
            "Todos os meses"
            if mes is None
            else meses[mes]
        ),
    )


# ============================================================
# RESUMO DE VENDAS
# ============================================================

summary = get_sales_summary_service(
    ano=ano_selecionado,
    mes=mes_selecionado,
)


quantidade_vendida = (
    float(summary["quantidade_vendida"])
    if summary["quantidade_vendida"] is not None
    else 0
)

receita_total = (
    float(summary["receita_total"])
    if summary["receita_total"] is not None
    else 0
)

lucro_total = (
    float(summary["lucro_total"])
    if summary["lucro_total"] is not None
    else 0
)

margem = (
    float(summary["margem"])
    if summary["margem"] is not None
    else 0
)


# ============================================================
# KPIs
# ============================================================

st.divider()

st.subheader("📈 Indicadores de Vendas")


col1, col2, col3, col4 = st.columns(4)


with col1:
    st.metric(
        "Quantidade Vendida",
        f"{quantidade_vendida:,.0f}",
    )


with col2:
    st.metric(
        "Receita",
        f"R$ {receita_total:,.2f}",
    )


with col3:
    st.metric(
        "Lucro",
        f"R$ {lucro_total:,.2f}",
    )


with col4:
    st.metric(
        "Margem",
        f"{margem:.2f}%",
    )


# ============================================================
# VENDAS POR MÊS
# ============================================================

st.divider()

st.subheader("📅 Evolução Mensal")


sales_by_month = get_sales_by_month_service()

df_month = pd.DataFrame(sales_by_month)


if not df_month.empty:

    df_month = df_month[
        df_month["ano"] == ano_selecionado
    ].copy()

    if not df_month.empty:

        numeric_columns = [
            "quantidade_vendida",
            "receita",
            "custo",
            "lucro",
        ]

        for column in numeric_columns:
            if column in df_month.columns:
                df_month[column] = df_month[column].astype(float)

        df_month["mes_nome"] = df_month["mes"].map(meses)

        df_month["periodo"] = (
            df_month["mes"].astype(str).str.zfill(2)
            + " - "
            + df_month["mes_nome"]
        )

        df_month = df_month.sort_values("mes")

        st.line_chart(
            df_month.set_index("periodo")["receita"]
        )

        col1, col2 = st.columns(2)

        with col1:

            st.caption("Receita mensal")

            st.bar_chart(
                df_month.set_index("periodo")["receita"],
                width="stretch",
            )

        with col2:

            st.caption("Lucro mensal")

            st.bar_chart(
                df_month.set_index("periodo")["lucro"],
                width="stretch",
            )

    else:

        st.info(
            "Não existem dados mensais para o ano selecionado."
        )

else:

    st.info(
        "Não existem dados disponíveis para evolução mensal."
    )


# ============================================================
# VENDAS POR PRODUTO
# ============================================================

st.divider()

st.subheader("🏆 Vendas por Produto")


sales_by_product = get_sales_by_product_service(
    ano=ano_selecionado,
    mes=mes_selecionado,
)

df_product = pd.DataFrame(sales_by_product)


if not df_product.empty:

    numeric_columns = [
        "quantidade_vendida",
        "receita",
        "lucro",
    ]

    for column in numeric_columns:
        if column in df_product.columns:
            df_product[column] = df_product[column].astype(float)

    col1, col2 = st.columns(2)

    with col1:

        st.caption("Top produtos por receita")

        top_products = (
            df_product
            .sort_values(
                "receita",
                ascending=False,
            )
            .head(10)
            .copy()
        )

        st.bar_chart(
            top_products.set_index(
                "nome_produto"
            )["receita"],
            width="stretch",
        )

    with col2:

        st.caption("Top produtos por quantidade")

        top_quantity = (
            df_product
            .sort_values(
                "quantidade_vendida",
                ascending=False,
            )
            .head(10)
            .copy()
        )

        st.bar_chart(
            top_quantity.set_index(
                "nome_produto"
            )["quantidade_vendida"],
            width="stretch",
        )

    st.subheader("Detalhamento por Produto")

    df_product_display = df_product.copy()

    df_product_display["margem"] = (
        (
            df_product_display["lucro"]
            / df_product_display["receita"]
        )
        .fillna(0)
        * 100
    )

    df_product_display = df_product_display[
        [
            "id_produto",
            "nome_produto",
            "quantidade_vendida",
            "receita",
            "lucro",
            "margem",
        ]
    ].copy()

    df_product_display.columns = [
        "ID",
        "Produto",
        "Quantidade",
        "Receita",
        "Lucro",
        "Margem (%)",
    ]

    st.dataframe(
        df_product_display,
        width="stretch",
        hide_index=True,
    )

else:

    st.info(
        "Não existem vendas de produtos para os filtros selecionados."
    )


# ============================================================
# VENDAS POR CLIENTE
# ============================================================

st.divider()

st.subheader("👥 Vendas por Cliente")


sales_by_customer = get_sales_by_customer_service(
    ano=ano_selecionado,
    mes=mes_selecionado,
)

df_customer = pd.DataFrame(sales_by_customer)


if not df_customer.empty:

    numeric_columns = [
        "quantidade_vendida",
        "receita",
        "lucro",
    ]

    for column in numeric_columns:
        if column in df_customer.columns:
            df_customer[column] = df_customer[column].astype(float)

    top_customers = (
        df_customer
        .sort_values(
            "receita",
            ascending=False,
        )
        .head(10)
        .copy()
    )

    st.bar_chart(
        top_customers.set_index(
            "nome_cliente"
        )["receita"],
        width="stretch",
    )

    st.subheader("Detalhamento por Cliente")

    df_customer_display = df_customer.copy()

    df_customer_display.columns = [
        "ID",
        "Cliente",
        "Quantidade",
        "Receita",
        "Lucro",
    ]

    st.dataframe(
        df_customer_display,
        width="stretch",
        hide_index=True,
    )

else:

    st.info(
        "Não existem vendas de clientes para os filtros selecionados."
    )


# ============================================================
# RODAPÉ
# ============================================================

st.divider()

st.caption(
    "Data Sales Platform | "
    "Pipeline ETL + Data Quality + Data Warehouse + Analytics"
)