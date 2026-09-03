"""API для работы с бронями."""

from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.dao.bookings import BookingDAO
from app.repositories.database import get_db
from app.repositories.schemas.bookings import BookingCreate, BookingResponse


bookings_router: APIRouter = APIRouter(
    prefix="/bookings",
    tags=["Bookings"],
)


@bookings_router.post(
    "",
    response_model=BookingResponse,
    status_code=status.HTTP_201_CREATED,
)
async def add_booking(
    booking: BookingCreate,
    db: AsyncSession = Depends(get_db),
) -> BookingResponse:
    """Создаёт новую бронь"""

    is_occupied: bool = await BookingDAO.has_active_booking(
        db,
        booking.booking_date,
        booking.booking_time,
    )

    if is_occupied:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Booking slot is already occupied",
        )

    return await BookingDAO.create(db, booking)


@bookings_router.get(
    "",
    response_model=list[BookingResponse],
)
async def get_bookings(
    booking_date: date | None = Query(default=None, alias="date"),
    db: AsyncSession = Depends(get_db),
) -> list[BookingResponse]:
    """Возвращает список броней"""

    return await BookingDAO.get_all(db, booking_date)


@bookings_router.get(
    "/{booking_id}",
    response_model=BookingResponse,
)
async def get_booking(
    booking_id: int = Path(..., gt=0),
    db: AsyncSession = Depends(get_db),
) -> BookingResponse:
    """Возвращает бронь по идентификатору"""

    booking = await BookingDAO.get_by_id(db, booking_id)

    if booking is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found",
        )

    return booking


@bookings_router.delete(
    "/{booking_id}",
    response_model=BookingResponse,
)
async def cancel_booking(
    booking_id: int = Path(..., gt=0),
    db: AsyncSession = Depends(get_db),
) -> BookingResponse:
    """Отменяет бронь без физического удаления"""

    booking = await BookingDAO.get_by_id(db, booking_id)

    if booking is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found",
        )

    return await BookingDAO.cancel(db, booking)
