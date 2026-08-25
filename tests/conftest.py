import os

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from scripts.seed_database import main as run_seed

TEST_DATABASE_URL = os.getenv(
    "ALEMBIC_DATABASE_URL",
    (
        "postgresql+psycopg2://"
        "data_sales_user:data_sales_password@"
        "localhost:5433/data_sales_test"
    ),
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


PIPELINE_TESTS = {
    "test_pipeline.py",
    "test_pipeline_integration.py",
}


def clear_database() -> None:
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
    test_file = request.node.path.name

    # Para testes do pipeline, limpa e popula o banco antes do teste
    if test_file in PIPELINE_TESTS:
        clear_database()
        run_seed()  # Executa o seed.py exatamente como está
        yield
        return

    # Para os demais testes (API / Banco unitário)
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