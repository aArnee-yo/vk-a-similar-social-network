import os

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from dotenv import find_dotenv, load_dotenv


# load_dotenv(find_dotenv())

# DB_URL = os.getenv('DB_URL')

DB_URL = "postgresql+asyncpg://vk:1234@localhost:5432/vk_db"

engine = create_async_engine(DB_URL, pool_size=20, max_overflow=0)

async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

class Base(DeclarativeBase):
    pass
