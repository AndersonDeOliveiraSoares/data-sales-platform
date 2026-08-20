from sqlalchemy import text

from tests.conftest import test_engine


def test_database_connection():
    with test_engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        assert result.scalar() == 1