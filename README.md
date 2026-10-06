# Booking service

Сервис бронирования мест на мероприятия: FastAPI, PostgreSQL, SQLAlchemy (async), Alembic, Redis.

## Запуск через Docker Compose

```bash
docker compose up --build
```

Compose поднимает:

| Сервис     | Назначение                                                      |
|------------|-----------------------------------------------------------------|
| `postgres` | PostgreSQL 18                                                   |
| `redis`    | Redis 7.2                                                       |
| `migrate`  | применяет миграции (`alembic upgrade head`) и загружает сиды     |
| `api`      | приложение на `http://127.0.0.1:8000`, стартует после `migrate` |

Документация API: `http://127.0.0.1:8000/docs`.
Проверки состояния: `GET /health/live`, `GET /health/ready` (проверяет доступность PostgreSQL).


## Конфигурация

Настройки читаются из переменных окружения и файла `.env` (пример в `.env.example`).

| Переменная           | Обязательная | Описание                                           |
|----------------------|--------------|----------------------------------------------------|
| `DATABASE_URL`       | нет          | DSN PostgreSQL (`postgresql+asyncpg://...`)        |
| `REDIS_URL`          | нет          | DSN Redis                                          |
| `JWT_SECRET`         | да           | секрет подписи JWT, не короче 32 символов          |
| `CORS_ALLOW_ORIGINS` | нет          | разрешённые origin через запятую; пусто — CORS выключен |

## Миграции

```bash
alembic revision --autogenerate -m "description"
alembic upgrade head
alembic downgrade -1
```

## Структура проекта

```
app/
  core/          конфигурация, ресурсы приложения
  db/            базовый класс моделей, движок и сессии
  models/        SQLAlchemy-модели
  schemas/       Pydantic-схемы
  repositories/  доступ к данным
  services/      бизнес-логика и границы транзакций
  routers/       HTTP-эндпоинты
alembic/         миграции
scripts/seed.py  сиды мероприятий (идемпотентные)
tests/
```

## Проверка кода

```bash
ruff check .
ruff format --check .
mypy app scripts alembic
```
