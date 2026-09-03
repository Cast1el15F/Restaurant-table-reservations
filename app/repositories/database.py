"""Подключение к базе данных"""

from collections.abc import AsyncGenerator

from sqlalchemy import Engine
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.core.config import DATABASE_URL


ASYNC_DATABASE_URL: str = DATABASE_URL.replace(
    "sqlite:///",
    "sqlite+aiosqlite:///",
)

engine: AsyncEngine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=False,
)

SessionLocal: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    """Базовый класс ORM-моделей"""

    pass


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Возвращает асинхронную сессию базы данных"""

    async with SessionLocal() as db:
        yield db
