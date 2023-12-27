import pytest
from sqlalchemy import text
from sqlalchemy.engine import Connection
from sqlalchemy.exc import ProgrammingError


def test_mysql_version(connection: Connection):
    version = connection.execute(text("select version()")).scalar()
    assert version == "8.2.0"


def test_exists_menus_table(connection: Connection):
    count = connection.execute(text("select count(1) from menus")).scalar()
    assert count == 0


def test_not_exists_table(connection: Connection):
    with pytest.raises(ProgrammingError) as e:
        connection.execute(text("select count(1) from mothers")).scalar()
    assert e.value.code == "f405"
