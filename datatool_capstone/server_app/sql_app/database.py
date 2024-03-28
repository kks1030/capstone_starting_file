from os import environ
from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base


DATABASE_URL = f"postgresql+asyncpg://{environ['VT_PGSQL_USER']}:{environ['VT_PGSQL_PASSWORD']}@{environ['VT_PGSQL_HOST']}/{environ['VT_PGSQL_DB']}"
#DATABASE_URL = f"sqlite+aiosqlite:///datatool_capstone.db"

engine = create_async_engine(
    DATABASE_URL,
    future=True,
    echo=True,
)

# expire_on_commit=False will prevent attributes from being expired
# after commit.
AsyncSessionFactory = async_sessionmaker(
    engine,
    autoflush=False,
    expire_on_commit=False,
)

Base = declarative_base()

# Dependency
async def get_db() -> AsyncGenerator:
    async with AsyncSessionFactory() as session:
        # logger.debug(f"ASYNC Pool: {engine.pool.status()}")
        print(f"ASYNC Pool: {engine.pool.status()}")
        yield session