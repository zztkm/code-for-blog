from sqlalchemy.engine import Connection
from sqlalchemy import text

def test_mysql_version(connection: Connection):
    version = connection.execute(text("select version()")).scalar()
    print(version)
    assert version == "8.2.0"