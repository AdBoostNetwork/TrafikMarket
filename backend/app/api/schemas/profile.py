from pydantic import BaseModel


class BalanceResponse(BaseModel):
    """Свободный баланс пользователя"""
    free_balance: float
