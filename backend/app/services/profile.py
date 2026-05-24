from datetime import datetime

from app.api.schemas.common import SuccessResponse
from app.api.schemas.profile import (
    BalanceResponse,
    DealTransaction,
    IOTransaction,
    RefTransaction,
    TransactionItem,
    TransactionsResponse,
    WallpaperCurrentResponse,
    WallpaperUpdateRequest,
)
from app.logger import get_logger
from app.repositories.profile import ProfileRepository

logger = get_logger(__name__)

_TRANSACTIONS_LIMIT = 20


class ProfileService:
    def __init__(self, repo: ProfileRepository) -> None:
        self._repo = repo

    async def get_balance(self, user_id: int) -> BalanceResponse:
        logger.info("Получение баланса | user_id=%s", user_id)
        row = await self._repo.get_balance(user_id)
        free_balance = row["current_balance"] - row["frozen_balance"]
        return BalanceResponse(free_balance=free_balance)

    async def get_wallpaper(self, user_id: int) -> WallpaperCurrentResponse:
        logger.info("Получение обоев пользователя | user_id=%s", user_id)
        row = await self._repo.get_wallpaper(user_id)
        return WallpaperCurrentResponse(wallpaper_id=row["wallpaper_id"], img_key=row["img_key"])

    async def get_transactions(self, user_id: int, cursor: str | None) -> TransactionsResponse:
        logger.info("Получение транзакций | user_id=%s | cursor=%s", user_id, cursor)
        cursor_ts, cursor_id = self._parse_cursor(cursor)
        rows = await self._repo.get_transactions(
            user_id=user_id,
            limit=_TRANSACTIONS_LIMIT,
            cursor_ts=cursor_ts,
            cursor_id=cursor_id,
        )
        items: list[TransactionItem] = [self._map_transaction(row) for row in rows]
        next_cursor = self._build_cursor(rows[-1]) if len(rows) == _TRANSACTIONS_LIMIT else None
        return TransactionsResponse(items=items, next_cursor=next_cursor)

    @staticmethod
    def _parse_cursor(cursor: str | None) -> tuple[datetime | None, int | None]:
        if cursor is None:
            return None, None
        ts_str, id_str = cursor.rsplit("_", 1)
        return datetime.fromisoformat(ts_str), int(id_str)

    @staticmethod
    def _build_cursor(row) -> str:
        ts: datetime = row["created_at"]
        return f"{ts.isoformat()}_{row['id']}"

    @staticmethod
    def _map_transaction(row) -> TransactionItem:
        kind = row["kind"]
        if kind == "io":
            return IOTransaction(
                kind="io",
                id=row["id"],
                created_at=row["created_at"],
                amount=row["amount"],
                type=row["type"],
            )
        if kind == "deal":
            return DealTransaction(
                kind="deal",
                id=row["id"],
                created_at=row["created_at"],
                amount=row["amount"],
                direction=row["direction"],
                announ_type=row["announ_type"],
            )
        return RefTransaction(
            kind="ref",
            id=row["id"],
            created_at=row["created_at"],
            amount=row["amount"],
            referral_name=row["referral_name"],
        )

    async def update_wallpaper(self, user_id: int, data: WallpaperUpdateRequest) -> SuccessResponse:
        logger.info("Изменение обоев пользователя | user_id=%s | wallpaper_id=%s", user_id, data.wallpaper_id)
        await self._repo.update_wallpaper(user_id, data.wallpaper_id)
        return SuccessResponse()
