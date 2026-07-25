from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from ai_assistant.db.main_session import make_main_session
from ai_assistant.logger import get_logger

logger = get_logger(__name__)

_main_session_factory: async_sessionmaker | None = None


def init_main_session_factory(main_database_url: str) -> None:
    global _main_session_factory
    _main_session_factory = make_main_session(main_database_url)
    logger.info("main_session_factory инициализирована")


async def get_main_session() -> AsyncGenerator[AsyncSession, None]:
    if _main_session_factory is None:
        raise RuntimeError("main_session_factory не инициализирована")
    async with _main_session_factory() as session:
        yield session


def get_main_session_factory() -> async_sessionmaker:
    if _main_session_factory is None:
        raise RuntimeError("main_session_factory не инициализирована")
    return _main_session_factory
