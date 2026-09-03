"""DAO для работы с бронями"""

from datetime import date, time

from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from app.repositories.models.bookings import Booking
from app.repositories.schemas.bookings import BookingCreate


class BookingDAO:
    """Объект доступа к данным броней"""

    @staticmethod
    def create(db: Session, booking_data: BookingCreate) -> Booking:
        """Создаёт и сохраняет бронь"""

        booking: Booking = Booking(
            **booking_data.model_dump(),
            status="active",
        )
        db.add(booking)
        db.commit()
        db.refresh(booking)

        return booking

    @staticmethod
    def get_all(
        db: Session,
        booking_date: date | None = None,
    ) -> list[Booking]:
        """Возвращает все брони с необязательной фильтрацией по дате"""

        query: Select[tuple[Booking]] = select(Booking).order_by(
            Booking.booking_date,
            Booking.booking_time,
        )

        if booking_date is not None:
            query = query.where(Booking.booking_date == booking_date)

        return list(db.scalars(query).all())

    @staticmethod
    def get_by_id(db: Session, booking_id: int) -> Booking | None:
        """Возвращает бронь по идентификатору"""

        return db.get(Booking, booking_id)

    @staticmethod
    def cancel(db: Session, booking: Booking) -> Booking:
        """Изменяет статус брони на cancelled"""

        booking.status = "cancelled"
        db.commit()
        db.refresh(booking)

        return booking

    @staticmethod
    def has_active_booking(
        db: Session,
        booking_date: date,
        booking_time: time,
    ) -> bool:
        """Проверяет занятость даты и времени"""

        query: Select[tuple[int]] = select(Booking.id).where(
            Booking.booking_date == booking_date,
            Booking.booking_time == booking_time,
            Booking.status == "active",
        )

        return db.scalar(query) is not None
