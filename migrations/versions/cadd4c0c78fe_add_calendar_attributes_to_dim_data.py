"""add calendar attributes to dim data

Revision ID: cadd4c0c78fe
Revises: a7932bd15096
Create Date: 2026-08-27
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.

revision: str = "cadd4c0c78fe"
down_revision: Union[str, Sequence[str], None] = "a7932bd15096"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    """Add calendar attributes to dw.dim_data."""

    op.add_column(
        "dim_data",
        sa.Column(
            "nome_mes",
            sa.String(length=20),
            nullable=True,
        ),
        schema="dw",
    )

    op.add_column(
        "dim_data",
        sa.Column(
            "dia_semana",
            sa.Integer(),
            nullable=True,
        ),
        schema="dw",
    )

    op.add_column(
        "dim_data",
        sa.Column(
            "nome_dia_semana",
            sa.String(length=20),
            nullable=True,
        ),
        schema="dw",
    )


def downgrade() -> None:
    """Remove calendar attributes from dw.dim_data."""

    op.drop_column(
        "dim_data",
        "nome_dia_semana",
        schema="dw",
    )

    op.drop_column(
        "dim_data",
        "dia_semana",
        schema="dw",
    )

    op.drop_column(
        "dim_data",
        "nome_mes",
        schema="dw",
    )
