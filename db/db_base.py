from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from config import settings as s


engine = create_async_engine(s.DB_URL)
session = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass
