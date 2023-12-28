from sqlalchemy import URL, Engine, create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


def create_db_url() -> URL:
    return URL.create(
        drivername="mysql+pymysql",
        username="mysql",
        password="mysql",
        host="localhost",
        port=3306,
        database="db",
    )


def create_db_engine(db_url: URL) -> Engine:
    return create_engine(db_url)


def create_session(engine: Engine):
    return sessionmaker(bind=engine, autocommit=False, autoflush=False)


SessionLocalFactory = create_session(create_db_engine(create_db_url()))
SessionLocal = scoped_session(SessionLocalFactory)
