"""create data warehouse schema

Revision ID: 2a0b8d0e0d56
Revises: 0ed064d629b8
Create Date: 2026-08-27
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2a0b8d0e0d56"
down_revision: Union[str, Sequence[str], None] = "0ed064d629b8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE SCHEMA IF NOT EXISTS dw")

    op.create_table(
        "dim_cliente",
        sa.Column("id_cliente", sa.Integer(), nullable=False),
        sa.Column("nome", sa.String(length=150), nullable=False),
        sa.Column("cidade", sa.String(length=100), nullable=True),
        sa.Column("estado", sa.String(length=2), nullable=True),
        sa.PrimaryKeyConstraint("id_cliente"),
        schema="dw",
    )

    op.create_table(
        "dim_produto",
        sa.Column("id_produto", sa.Integer(), nullable=False),
        sa.Column("nome_produto", sa.String(length=150), nullable=False),
        sa.Column("categoria", sa.String(length=100), nullable=False),
        sa.Column("subcategoria", sa.String(length=100), nullable=True),
        sa.Column(
            "preco_custo",
            sa.Numeric(precision=12, scale=2),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id_produto"),
        schema="dw",
    )

    op.create_table(
        "dim_data",
        sa.Column("data", sa.Date(), nullable=False),
        sa.Column("ano", sa.Integer(), nullable=False),
        sa.Column("mes", sa.Integer(), nullable=False),
        sa.Column("trimestre", sa.Integer(), nullable=False),
        sa.Column("dia", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("data"),
        schema="dw",
    )

    op.create_table(
        "fact_vendas",
        sa.Column(
            "id_item_pedido",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "id_pedido",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "id_cliente",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "id_produto",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column("data", sa.Date(), nullable=False),
        sa.Column("ano", sa.Integer(), nullable=False),
        sa.Column("mes", sa.Integer(), nullable=False),
        sa.Column(
            "trimestre",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column("dia", sa.Integer(), nullable=False),
        sa.Column(
            "quantidade",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "preco_unitario",
            sa.Numeric(precision=12, scale=2),
            nullable=False,
        ),
        sa.Column(
            "preco_custo",
            sa.Numeric(precision=12, scale=2),
            nullable=False,
        ),
        sa.Column(
            "subtotal",
            sa.Numeric(precision=12, scale=2),
            nullable=False,
        ),
        sa.Column(
            "custo_total",
            sa.Numeric(precision=12, scale=2),
            nullable=False,
        ),
        sa.Column(
            "receita",
            sa.Numeric(precision=12, scale=2),
            nullable=False,
        ),
        sa.Column(
            "lucro",
            sa.Numeric(precision=12, scale=2),
            nullable=False,
        ),
        sa.Column(
            "margem",
            sa.Numeric(precision=12, scale=6),
            nullable=False,
        ),
        sa.Column(
            "valor_frete",
            sa.Numeric(precision=12, scale=2),
            nullable=False,
        ),
        sa.Column(
            "status_pedido",
            sa.String(length=20),
            nullable=False,
        ),
        sa.Column(
            "forma_pagamento",
            sa.String(length=30),
            nullable=False,
        ),
        sa.Column(
            "nome",
            sa.String(length=150),
            nullable=False,
        ),
        sa.Column(
            "cidade",
            sa.String(length=100),
            nullable=True,
        ),
        sa.Column(
            "estado",
            sa.String(length=2),
            nullable=True,
        ),
        sa.Column(
            "nome_produto",
            sa.String(length=150),
            nullable=False,
        ),
        sa.Column(
            "categoria",
            sa.String(length=100),
            nullable=False,
        ),
        sa.Column(
            "subcategoria",
            sa.String(length=100),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id_item_pedido"),
        schema="dw",
    )


def downgrade() -> None:
    op.drop_table("fact_vendas", schema="dw")
    op.drop_table("dim_data", schema="dw")
    op.drop_table("dim_produto", schema="dw")
    op.drop_table("dim_cliente", schema="dw")
    op.execute("DROP SCHEMA IF EXISTS dw CASCADE")