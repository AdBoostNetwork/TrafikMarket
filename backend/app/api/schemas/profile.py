from datetime import datetime
from decimal import Decimal
from typing import Annotated, Literal

from pydantic import BaseModel, Field


class AssetsResponse(BaseModel):
    """Активы пользователя"""
    current_balance: Decimal
    frozen_balance: Decimal
    total_balance: Decimal


class BalanceResponse(BaseModel):
    """Свободный баланс пользователя"""
    free_balance: Decimal


class WallpaperCurrentResponse(BaseModel):
    """Текущие обои пользователя"""
    wallpaper_id: int | None
    img_key: str | None


class WallpaperUpdateRequest(BaseModel):
    """Запрос на изменение обоев пользователя"""
    wallpaper_id: int


class IOTransaction(BaseModel):
    """Пополнение или вывод средств"""
    kind: Literal["io"]
    id: int
    created_at: datetime
    amount: Decimal
    type: str  # "in" — пополнение, "out" — вывод


class DealTransaction(BaseModel):
    """Транзакция сделки"""
    kind: Literal["deal"]
    id: int
    created_at: datetime
    amount: Decimal
    direction: str   # "buy" — покупка, "sell" — продажа
    announ_type: str  # тип товара из announ_types


class RefTransaction(BaseModel):
    """Реферальное вознаграждение"""
    kind: Literal["ref"]
    id: int
    created_at: datetime
    amount: Decimal
    referral_name: str  # имя реферала из users.name


TransactionItem = Annotated[
    IOTransaction | DealTransaction | RefTransaction,
    Field(discriminator="kind"),
]


class TransactionsResponse(BaseModel):
    """Список транзакций пользователя с курсором для следующей страницы"""
    items: list[TransactionItem]
    next_cursor: str | None
