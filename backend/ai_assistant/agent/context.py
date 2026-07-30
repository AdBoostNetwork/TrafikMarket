from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession


@dataclass(frozen=True)
class ToolContext:
    user_id: int
    db: AsyncSession        # read-only сессия основной БД (traffmarket)
    ai_db: AsyncSession     # read-write сессия своей БД (traffmarket_ai)
