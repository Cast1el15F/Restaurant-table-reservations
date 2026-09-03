"""Pydantic-схемы броней"""

import re
from datetime import date, datetime, time, timedelta
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


def get_example_datetime() -> tuple[str, str]:
    """Возвращает текущую дату и ближайший допустимый часовой слот"""

    current: datetime = datetime.now()

    if current.hour < 12:
        booking_date: date = current.date()
        booking_hour: int = 12
    elif current.hour >= 22:
        booking_date = current.date() + timedelta(days=1)
        booking_hour = 12
    else:
        booking_date = current.date()
        booking_hour = current.hour + 1

    return booking_date.isoformat(), f"{booking_hour:02d}:00"


_example_date: str
_example_time: str
_example_date, _example_time = get_example_datetime()


class BookingCreate(BaseModel):
    """Схема создания брони"""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Иван Иванов",
                "phone": "+79991234567",
                "booking_date": _example_date,
                "booking_time": _example_time,
                "guests": 2,
            },
        },
    )

    name: str = Field(min_length=2)
    phone: str
    booking_date: date
    booking_time: time
    guests: int = Field(ge=1, le=12)

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        """Проверяет имя гостя"""

        value = value.strip()

        if len(value) < 2:
            raise ValueError("Имя должно содержать минимум 2 символа")

        if not all(char.isalpha() or char in " -" for char in value):
            raise ValueError("Имя может содержать только буквы, пробелы и дефис")

        if value[0] in " -" or value[-1] in " -":
            raise ValueError("Имя не может начинаться или заканчиваться пробелом")

        return value

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value: str) -> str:
        """Проверяет российский формат телефона"""

        if not re.fullmatch(r"(?:\+7|8)\d{10}", value):
            raise ValueError(
                "Телефон должен быть в формате +7XXXXXXXXXX или 8XXXXXXXXXX",
            )

        return value

    @field_validator("booking_date")
    @classmethod
    def validate_booking_date(cls, value: date) -> date:
        """Проверяет допустимый диапазон даты бронирования"""

        today: date = date.today()
        max_date: date = today + timedelta(days=90)

        if not today <= value <= max_date:
            raise ValueError(
                "Дата должна быть от сегодняшнего дня до 90 дней вперёд",
            )

        return value

    @field_validator("booking_time")
    @classmethod
    def validate_booking_time(cls, value: time) -> time:
        """Проверяет допустимый часовой слот"""

        if (
            value.hour < 12
            or value.hour > 22
            or value.minute != 0
            or value.second != 0
            or value.microsecond != 0
        ):
            raise ValueError("Доступны только слоты с 12:00 до 22:00")

        return value


class BookingResponse(BookingCreate):
    """Схема ответа с данными брони"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    status: Literal["active", "cancelled"]
