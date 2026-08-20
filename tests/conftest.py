import os

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from src.database.connection import Base


TEST_DATABASE_URL = os.getenv(
    "ALEMBIC_DATABASE_URL",
    "postgresql+psycopg2://data_sales_user:data_sales_password@localhost:5433/data_sales_test",
)


test_engine = create_engine(
    TEST_DATABASE_URL,
    echo=False,
)


SessionTest = sessionmaker(
    bind=test_engine,
    autoflush=False,
    autocommit=False,
)


@pytest.fixture(autouse=True)
def clean_database():
    with test_engine.begin() as connection:
        connection.execute(
            text(
                """
                TRUNCATE TABLE
                    item_pedido,
                    pedido,
                    produto,
                    cliente
                RESTART IDENTITY CASCADE
                """
            )
        )

    yield


@pytest.fixture
def db():
    session = SessionTest()

    try:
        yield session
    finally:
        session.rollback()
        session.close()