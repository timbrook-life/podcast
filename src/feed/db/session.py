import yaml
import psycopg2
from contextlib import contextmanager
from src.config import DynamicConfig
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
from sqlalchemy.pool import QueuePool


def getconn():
    conf = DynamicConfig().db_connection()
    print("getconnection!")
    return psycopg2.connect(
        user=conf.username,
        password=conf.password,
        host=conf.host,
        port=conf.port,
        dbname="notification",
        sslmode="require",
    )


mypool = QueuePool(getconn, max_overflow=5, pool_size=2)

engine = create_engine("postgresql://", pool=mypool)

# Exports
Session = sessionmaker(bind=engine)
Base = declarative_base()


@contextmanager
def get_session():
    session = Session()
    yield session
    session.close()

