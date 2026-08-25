import os

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker


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


def clear_database():
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


@pytest.fixture(autouse=True)
def clean_database(request):

    test_file = request.node.fspath.basename

    pipeline_tests = {
        "test_pipeline.py",
        "test_pipeline_integration.py",
    }

    if test_file in pipeline_tests:
        yield
        return

    clear_database()

    yield

    clear_database()


@pytest.fixture
def db():
    session = SessionTest()

    try:
        yield session
    finally:
        session.rollback()
        session.close()