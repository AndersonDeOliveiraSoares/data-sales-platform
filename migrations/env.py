from logging.config import fileConfig

from alembic import context
from sqlalchemy import create_engine, pool

import os

from src.database.connection import Base, DATABASE_URL

# Importante: importar os modelos para registrá-los no Base.metadata
from src.database.models.cliente import Cliente
from src.database.models.produto import Produto
from src.database.models.pedido import Pedido
from src.database.models.item_pedido import ItemPedido


config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


target_metadata = Base.metadata
DATABASE_URL = os.getenv("ALEMBIC_DATABASE_URL", DATABASE_URL)

def run_migrations_offline() -> None:
    """Executa as migrations em modo offline."""

    url = DATABASE_URL

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Executa as migrations conectando diretamente ao banco."""

    connectable = create_engine(
        DATABASE_URL,
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()