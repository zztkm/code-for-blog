from collections.abc import Generator
from uuid import uuid4

import pytest
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker
from testcontainers.mysql import MySqlContainer

from src.udonya import app, get_db

from .factories import MenusFactory


class TestingSession(Session):
    def commit(self):
        self.flush()

@pytest.fixture(scope="session")
def mysql() -> MySqlContainer:
    """MySQLコンテナのフィクスチャです。

    engineから呼び出されるため、通常は他のテストから呼び出されません。

    Returns
    -------
        MySqlContainer:
    """
    mysql = MySqlContainer(
        image="udon-db:latest",
    )
    mysql.start()
    return mysql
    # NOTE: pytestが正常に終了したら、自動的に停止します。


@pytest.fixture(scope="session")
def engine(mysql: MySqlContainer) -> Engine:
    """MySQLコンテナから SQLAlchemy の Engine を作成します。
    connectionから呼び出されるため、通常は他のテストから呼び出されません。

    Args:
    ----
        mysql (MySqlContainer): MySQLコンテナのfixture

    Returns:
    -------
        Engine: SQLAlchemy の Engine
    """
    return create_engine(mysql.get_connection_url())


@pytest.fixture()
def connection(engine: Engine):
    """この関数は、データベースエンジンへの接続を作成し、接続オブジェクトをyieldします。
    yieldステートメントの後、トランザクションをロールバックし、接続を閉じます。

    Args:
    ----
        engine (Engine): SQLAlchemyエンジンオブジェクト。

    Yields:
    ------
        Connection: SQLAlchemy接続オブジェクト。
    """
    connection = engine.connect()
    yield connection
    connection.rollback()
    connection.close()


@pytest.fixture(scope="session")
def create_session_factory(engine: Engine):
    return sessionmaker(bind=engine, autocommit=False, autoflush=True, class_=TestingSession)


@pytest.fixture()
def test_db(create_session_factory: sessionmaker[Session]) -> Generator[Session, None, None]:
    TestSessionLocal = scoped_session(create_session_factory, scopefunc=lambda: uuid4().hex)
    session = TestSessionLocal()

    MenusFactory._meta.sqlalchemy_session = session

    def override_get_db():
        try:
            yield session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    yield session

    session.rollback()
    session.close()
