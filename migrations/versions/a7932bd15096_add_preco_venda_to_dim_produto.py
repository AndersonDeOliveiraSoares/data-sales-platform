"""add preco venda to dim produto

Revision ID: a7932bd15096
Revises: 2a0b8d0e0d56
Create Date: 2026-08-27 19:11:57.960957

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.

revision: str = "a7932bd15096"
down_revision: Union[str, Sequence[str], None] = "2a0b8d0e0d56"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    """Add preco_venda to dw.dim_produto."""

    op.add_column(
        "dim_produto",
        sa.Column(
            "preco_venda",
            sa.Numeric(
                precision=12,
                scale=2,
            ),
            nullable=True,
        ),
        schema="dw",
    )

def downgrade() -> None:
    """Remove preco_venda from dw.dim_produto."""


    op.drop_column(
        "dim_produto",
        "preco_venda",
        schema="dw",
    )

