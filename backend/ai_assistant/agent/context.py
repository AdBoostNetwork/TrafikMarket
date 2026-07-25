from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession


@dataclass(frozen=True)
class ToolContext:
    user_id: int
    db: AsyncSession
