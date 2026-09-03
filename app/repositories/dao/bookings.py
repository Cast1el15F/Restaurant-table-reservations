"""DAO для работы с бронями"""

from datetime import date, time

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.models.bookings import Booking
from app.repositories.schemas.bookings import BookingCreate


class BookingDAO:
    """Объект доступа к данным броней"""

    @staticmethod
    async def create(
        db: AsyncSession,
        booking_data: BookingCreate,
    ) -> Booking:
        """Создаёт и сохраняет бронь"""

        booking: Booking = Booking(
            **booking_data.model_dump(),
            status="active",
        )

        db.add(booking)
        await db.commit()
        await db.refresh(booking)

        return booking

    @staticmethod
    async def get_all(
        db: AsyncSession,
        booking_date: date | None = None,
    ) -> list[Booking]:
        """Возвращает все брони с необязательной фильтрацией по дате"""

        query: Select[tuple[Booking]] = select(Booking).order_by(
            Booking.booking_date,
            Booking.booking_time,
        )

        if booking_date is not None:
            query = query.where(Booking.booking_date == booking_date)

        result = await db.scalars(query)

        return list(result.all())

    @staticmethod
    async def get_by_id(
        db: AsyncSession,
        booking_id: int,
    ) -> Booking | None:
        """Возвращает бронь по идентификатору"""

        return await db.get(Booking, booking_id)

    @staticmethod
    async def cancel(
        db: AsyncSession,
        booking: Booking,
    ) -> Booking:
        """Изменяет статус брони на cancelled"""

        booking.status = "cancelled"

        await db.commit()
        await db.refresh(booking)

        return booking

    @staticmethod
    async def has_active_booking(
        db: AsyncSession,
        booking_date: date,
        booking_time: time,
    ) -> bool:
        """Проверяет занятость даты и времени"""

        query: Select[tuple[int]] = select(Booking.id).where(
            Booking.booking_date == booking_date,
            Booking.booking_time == booking_time,
            Booking.status == "active",
        )

        booking_id: int | None = await db.scalar(query)

        return booking_id is not None
