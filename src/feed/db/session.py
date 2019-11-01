from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
import connection


engine = create_engine(
    URL(
        "postgresql",
        username=connection.USERNAME,
        password=connection.PASSWORD,
        host=connection.HOST,
        port=connection.PORT,
        database="notification",
    ),
    connect_args={"sslmode": "require"},
)

# Exports
Session = sessionmaker(bind=engine)
Base = declarative_base()

