"""Подключение к базе данных"""

from collections.abc import Generator

from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import DATABASE_URL


engine: Engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal: sessionmaker[Session] = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)


class Base(DeclarativeBase):
    """Базовый класс ORM-моделей"""

    pass


def get_db() -> Generator[Session, None, None]:
    """Возвращает сессию базы данных для запроса"""

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
