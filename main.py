"""Файл запуска проекта."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.api.bookings import bookings_router
from app.repositories.database import Base, engine
from app.repositories.models.bookings import Booking


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Создаёт таблицы базы данных при запуске приложения"""

    Base.metadata.create_all(bind=engine)
    yield


app: FastAPI = FastAPI(lifespan=lifespan)

app.include_router(bookings_router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
