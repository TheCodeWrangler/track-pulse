from google.cloud.sql.connector import Connector, IPTypes, create_async_connector
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession
import asyncpg
import os
import logging
from typing import AsyncGenerator, Any

logging.basicConfig(level=logging.INFO)


# Dependency to get the database session
async def get_db() -> AsyncGenerator[AsyncSession, Any]:
    connector = await create_async_connector()
    pool = await connect_with_connector(connector)

    AsyncSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=pool,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    try:
        async with AsyncSessionLocal() as session:
            async with session.begin():
                yield session
    finally:
        # await db.close
        # close Connector
        await connector.close_async()

        # dispose of connection pool
        await pool.dispose()


async def create_db_and_tables() -> None:
    """
    Creates the database and tables if they do not already exist.
    """
    connector = await create_async_connector()
    engine = await connect_with_connector(connector)
    # example query
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
        logging.info("Database and tables created")

    # close Connector
    await connector.close_async()

    # dispose of connection pool
    await engine.dispose()


async def connect_with_connector(connector: Connector) -> AsyncEngine:
    instance_connection_name = os.environ[
        "INSTANCE_CONNECTION_NAME"
    ]  # e.g. 'project:region:instance'
    db_user = os.environ["DB_USER"]  # e.g. 'my-db-user'
    db_pass = os.environ["DB_PASS"]  # e.g. 'my-db-password'
    db_name = os.environ["DB_NAME"]  # e.g. 'my-database'

    ip_type = IPTypes.PRIVATE if os.environ.get("PRIVATE_IP") else IPTypes.PUBLIC
    logging.debug(f"Connection to {instance_connection_name} with {ip_type}")

    # initialize Connector object for connections to Cloud SQL
    async def getconn() -> asyncpg.Connection:
        conn: asyncpg.Connection = await connector.connect_async(
            instance_connection_name,  # Cloud SQL instance connection name
            "asyncpg",
            user=db_user,
            password=db_pass,
            db=db_name,
            ip_type=ip_type,
        )
        return conn

    # The Cloud SQL Python Connector can be used along with SQLAlchemy using the
    # 'async_creator' argument to 'create_async_engine'
    pool = create_async_engine(
        "postgresql+asyncpg://",
        async_creator=getconn,
    )
    return pool


def connect_local() -> AsyncEngine:
    # The Cloud SQL Python Connector can be used along with SQLAlchemy using the
    # 'async_creator' argument to 'create_async_engine'
    async def getconn() -> asyncpg.Connection:
        conn: asyncpg.Connection = await asyncpg.connect(
            user="postgres", password="postgres", database="postgres", host="localhost"
        )
        return conn

    pool = create_async_engine(
        "postgresql+asyncpg://",
        async_creator=getconn,
    )
    return pool
