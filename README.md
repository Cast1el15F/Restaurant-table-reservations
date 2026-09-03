# Restaurant Table Reservations

REST API для бронирования столиков в ресторане

## Стек

- Python 3.11+
- FastAPI
- Pydantic v2
- SQLAlchemy 2.0
- SQLite
- Uvicorn
- Poetry

## Установка

```bash
poetry install
```

## Конфигурация

Создайте файл `.env` в корне проекта:

```env
DATABASE_URL=sqlite:///./restaurant.db
```

Таблица `bookings` создаётся автоматически при запуске приложения.

## Запуск

```bash
poetry run uvicorn main:app --reload
```

API будет доступно по адресу:

```text
http://127.0.0.1:8000
```

Документация:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Эндпоинты

| Метод | URL | Описание |
|---|---|---|
| POST | `/bookings` | Создание брони |
| GET | `/bookings` | Получение списка броней |
| GET | `/bookings?date=2026-08-20` | Фильтрация по дате |
| GET | `/bookings/{booking_id}` | Получение брони по идентификатору |
| DELETE | `/bookings/{booking_id}` | Отмена брони без удаления записи |

## Формат запроса

```json
{
  "name": "Иван Иванов",
  "phone": "+79991234567",
  "booking_date": "2026-09-10",
  "booking_time": "15:00",
  "guests": 2
}
```

## Валидация

- `name` — минимум 2 символа, буквы, пробелы и дефис
- `phone` — формат `+7XXXXXXXXXX` или `8XXXXXXXXXX`
- `booking_date` — от сегодняшнего дня до 90 дней вперёд
- `booking_time` — слоты с `12:00` до `22:00`
- `guests` — от 1 до 12

## Статусы ответов

- `201` — бронь создана
- `200` — успешное получение или отмена
- `404` — бронь не найдена
- `409` — слот уже занят
- `422` — ошибка валидации

## Статусы брони

- `active` — активная бронь
- `cancelled` — отменённая бронь

## Структура проекта

```text
app/
├── api/
│   └── bookings.py
├── core/
│   └── config.py
└── repositories/
    ├── dao/
    │   └── bookings.py
    ├── models/
    │   └── bookings.py
    ├── schemas/
    │   └── bookings.py
    └── database.py
main.py
pyproject.toml
README.md
```

## Принятые решения

SQLite выбрана для простого локального запуска без отдельного сервера базы данных. SQLAlchemy используется для работы с ORM-моделями, а Pydantic — для типизации и валидации входных данных. Отмена брони изменяет статус на `cancelled`, поэтому запись сохраняется в базе данных. Эндпоинты, DAO, схемы и модели разделены по отдельным слоям.

## Что можно улучшить

- добавить сервисный слой
- добавить Alembic-миграции
- написать тесты на pytest и httpx
- добавить пагинацию
- добавить Dockerfile и CI