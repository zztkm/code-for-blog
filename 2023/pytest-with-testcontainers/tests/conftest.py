import pytest
from sqlalchemy import Engine, create_engine
from testcontainers.mysql import MySqlContainer


@pytest.fixture(scope="session")
def mysql() -> MySqlContainer:
    """MySQLコンテナのフィクスチャです。
    engineから呼び出されるため、通常は他のテストから呼び出されません。

    Returns:
        MySqlContainer:
    """
    mysql = MySqlContainer(
        image="mysql:8.2.0",
    )
    return mysql.start()
    # NOTE: pytestが正常に終了したら、自動的に停止します。


@pytest.fixture(scope="session")
def engine(mysql: MySqlContainer) -> Engine:
    """
    MySQLコンテナから SQLAlchemy の Engine を作成します。
    connectionから呼び出されるため、通常は他のテストから呼び出されません。

    Args:
        mysql (MySqlContainer): MySQLコンテナのfixture

    Returns:
        Engine: SQLAlchemy の Engine
    """
    return create_engine(mysql.get_connection_url())


@pytest.fixture(scope="function")
def connection(engine: Engine):
    """
    この関数は、データベースエンジンへの接続を作成し、接続オブジェクトをyieldします。
    yieldステートメントの後、トランザクションをロールバックし、接続を閉じます。

    Args:
        engine (Engine): SQLAlchemyエンジンオブジェクト。

    Yields:
        Connection: SQLAlchemy接続オブジェクト。
    """
    connection = engine.connect()
    yield connection
    connection.rollback()
    connection.close()
