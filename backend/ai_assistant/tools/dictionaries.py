from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from ai_assistant.logger import get_logger

logger = get_logger(__name__)

_SPEC = {
    "platform": ("platforms", "platform_name"),
    "traffic_type": ("traffic_types", "traffic_type_name"),
    "audience": ("audience_types", "type_name"),
}

_dicts: dict[str, list[str]] = {}


async def load_dictionaries(session: AsyncSession) -> None:
    for key, (table, column) in _SPEC.items():
        result = await session.execute(text(f"SELECT {column} FROM {table} ORDER BY id"))
        _dicts[key] = list(result.scalars().all())
    logger.info(
        "справочники загружены | %s",
        " | ".join(f"{key}={len(values)}" for key, values in _dicts.items()),
    )


def get_dictionary(key: str) -> list[str]:
    return list(_dicts.get(key, []))
