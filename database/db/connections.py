from google.cloud.sql.connector import Connector, IPTypes
from sqlalchemy.orm import Session, sessionmaker
from sqlmodel import SQLModel
import pg8000
import os
import logging
from typing import Generator, Any
import sqlalchemy

logging.basicConfig(level=logging.INFO)


# Dependency to get the database session
def get_db(local=False) -> Generator[Session, Any, None]:

    if local:
        engine = connect_local()
    else:
        engine = connect_with_connector()
    sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    db = sessionLocal()

    try:
        yield db
    finally:
        db.close()


def create_db_and_tables(local=False) -> None:
    """
    Creates the database and tables if they do not already exist.
    """
    if local:
        engine = connect_local()
    else:
        engine = connect_with_connector()
    SQLModel.metadata.create_all(engine)


def connect_with_connector() -> sqlalchemy.engine.base.Engine:
    """
    Initializes a connection pool for a Cloud SQL instance of Postgres.

    Uses the Cloud SQL Python Connector package.
    """
    # Note: Saving credentials in environment variables is convenient, but not
    # secure - consider a more secure solution such as
    # Cloud Secret Manager (https://cloud.google.com/secret-manager) to help
    # keep secrets safe.

    instance_connection_name = os.environ[
        "INSTANCE_CONNECTION_NAME"
    ]  # e.g. 'project:region:instance'
    db_user = os.environ["DB_USER"]  # e.g. 'my-db-user'
    db_pass = os.environ["DB_PASS"]  # e.g. 'my-db-password'
    db_name = os.environ["DB_NAME"]  # e.g. 'my-database'

    ip_type = IPTypes.PRIVATE if os.environ.get("PRIVATE_IP") else IPTypes.PUBLIC
    logging.debug(f"Connection to {instance_connection_name} with {ip_type}")
    # initialize Cloud SQL Python Connector object
    connector = Connector()

    def getconn() -> pg8000.dbapi.Connection:
        conn: pg8000.dbapi.Connection = connector.connect(
            instance_connection_name,
            "pg8000",
            user=db_user,
            password=db_pass,
            db=db_name,
            ip_type=ip_type,
        )
        return conn

    # The Cloud SQL Python Connector can be used with SQLAlchemy
    # using the 'creator' argument to 'create_engine'
    pool = sqlalchemy.create_engine(
        "postgresql+pg8000://",
        creator=getconn,
        # ...
    )
    return pool


def connect_local() -> sqlalchemy.engine.base.Engine:

    db_user = "postgres"  # e.g. 'my-db-user'
    db_pass = "postgres"  # e.g. 'my-db-password'
    db_name = "postgres"  # e.g. 'my-database'

    # initialize Cloud SQL Python Connector object

    #  Create SQLAlchemy engine
    def getconn() -> pg8000.dbapi.Connection:
        conn: pg8000.dbapi.Connection = pg8000.connect(
            user=db_user, password=db_pass, database=db_name, host="localhost"
        )
        return conn

    pool = sqlalchemy.create_engine(
        "postgresql+pg8000://",
        creator=getconn,
        # ...
    )
    return pool
