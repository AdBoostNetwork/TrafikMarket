from dataclasses import dataclass

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


@dataclass(frozen=True)
class MessageRow:
    role: str
    content: str


@dataclass(frozen=True)
class FactRow:
    id: int
    content: str


_SQL_FIND_CURRENT_DIALOG = text(
    "SELECT id FROM dialogs "
    "WHERE user_id = :user_id "
    "AND last_message_at >= now() - (:pause_seconds * interval '1 second') "
    "ORDER BY last_message_at DESC LIMIT 1"
)
_SQL_CREATE_DIALOG = text("INSERT INTO dialogs (user_id) VALUES (:user_id) RETURNING id")
_SQL_INSERT_MESSAGE = text(
    "INSERT INTO messages (dialog_id, role, content) VALUES (:dialog_id, :role, :content)"
)
_SQL_TOUCH_DIALOG = text("UPDATE dialogs SET last_message_at = now() WHERE id = :dialog_id")
_SQL_RECENT_MESSAGES = text(
    "SELECT role, content FROM ("
    "SELECT id, role, content FROM messages "
    "WHERE dialog_id = :dialog_id ORDER BY id DESC LIMIT :limit"
    ") AS sub ORDER BY id ASC"
)
_SQL_GET_FACTS = text("SELECT id, content FROM user_facts WHERE user_id = :user_id ORDER BY id")
_SQL_ADD_FACT = text("INSERT INTO user_facts (user_id, content) VALUES (:user_id, :content) RETURNING id")
_SQL_UPDATE_FACT = text(
    "UPDATE user_facts SET content = :content WHERE id = :fact_id AND user_id = :user_id"
)
_SQL_DELETE_FACT = text("DELETE FROM user_facts WHERE id = :fact_id AND user_id = :user_id")


async def get_or_create_current_dialog(session: AsyncSession, user_id: int, pause_seconds: int) -> int:
    result = await session.execute(
        _SQL_FIND_CURRENT_DIALOG, {"user_id": user_id, "pause_seconds": pause_seconds}
    )
    dialog_id = result.scalar_one_or_none()
    if dialog_id is not None:
        return dialog_id

    result = await session.execute(_SQL_CREATE_DIALOG, {"user_id": user_id})
    return result.scalar_one()


async def add_message(session: AsyncSession, dialog_id: int, role: str, content: str) -> None:
    await session.execute(_SQL_INSERT_MESSAGE, {"dialog_id": dialog_id, "role": role, "content": content})
    await session.execute(_SQL_TOUCH_DIALOG, {"dialog_id": dialog_id})


async def get_recent_messages(session: AsyncSession, dialog_id: int, limit: int) -> list[MessageRow]:
    result = await session.execute(_SQL_RECENT_MESSAGES, {"dialog_id": dialog_id, "limit": limit})
    return [MessageRow(role=row["role"], content=row["content"]) for row in result.mappings()]


async def get_facts(session: AsyncSession, user_id: int) -> list[FactRow]:
    result = await session.execute(_SQL_GET_FACTS, {"user_id": user_id})
    return [FactRow(id=row["id"], content=row["content"]) for row in result.mappings()]


async def add_fact(session: AsyncSession, user_id: int, content: str) -> int:
    result = await session.execute(_SQL_ADD_FACT, {"user_id": user_id, "content": content})
    return result.scalar_one()


async def update_fact(session: AsyncSession, user_id: int, fact_id: int, content: str) -> bool:
    result = await session.execute(
        _SQL_UPDATE_FACT, {"fact_id": fact_id, "user_id": user_id, "content": content}
    )
    return result.rowcount > 0


async def delete_fact(session: AsyncSession, user_id: int, fact_id: int) -> bool:
    result = await session.execute(_SQL_DELETE_FACT, {"fact_id": fact_id, "user_id": user_id})
    return result.rowcount > 0
