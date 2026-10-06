from dataclasses import dataclass
from typing import Self

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from app.core.config import Settings
from app.db.session import create_engine, create_session_factory


@dataclass(frozen=True, slots=True)
class AppResources:
    settings: Settings
    engine: AsyncEngine
    session_factory: async_sessionmaker[AsyncSession]

    @classmethod
    def create(cls, settings: Settings) -> Self:
        engine = create_engine(settings)
        return cls(
            settings=settings,
            engine=engine,
            session_factory=create_session_factory(engine),
        )

    async def close(self) -> None:
        await self.engine.dispose()
