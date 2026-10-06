import asyncio
import logging
from datetime import UTC, datetime
from typing import Any

from sqlalchemy.dialects.postgresql import insert

from app.core.config import get_settings
from app.db.session import create_engine
from app.models import Event

logger = logging.getLogger(__name__)

EVENTS: list[dict[str, Any]] = [
    {
        "slug": "python-meetup",
        "title": "Python Meetup",
        "starts_at": datetime(2026, 12, 5, 18, 0, tzinfo=UTC),
        "capacity": 10,
    },
    {
        "slug": "fastapi-workshop",
        "title": "FastAPI Workshop",
        "starts_at": datetime(2026, 12, 12, 10, 0, tzinfo=UTC),
        "capacity": 30,
    },
    {
        "slug": "postgres-conf",
        "title": "PostgreSQL Conference",
        "starts_at": datetime(2027, 2, 20, 9, 0, tzinfo=UTC),
        "capacity": 200,
    },
    {
        "slug": "jazz-evening",
        "title": "Jazz Evening",
        "starts_at": datetime(2026, 11, 28, 20, 0, tzinfo=UTC),
        "capacity": 50,
    },
    {
        "slug": "chess-masterclass",
        "title": "Chess Masterclass",
        "starts_at": datetime(2026, 12, 19, 15, 0, tzinfo=UTC),
        "capacity": 5,
    },
]


async def seed() -> int:
    engine = create_engine(get_settings())
    try:
        async with engine.begin() as connection:
            result = await connection.execute(
                insert(Event)
                .values(EVENTS)
                .on_conflict_do_nothing(index_elements=[Event.slug])
                .returning(Event.id)
            )
            return len(result.all())
    finally:
        await engine.dispose()


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    created = asyncio.run(seed())
    logger.info("Seeded events: %d created, %d already existed", created, len(EVENTS) - created)


if __name__ == "__main__":
    main()
