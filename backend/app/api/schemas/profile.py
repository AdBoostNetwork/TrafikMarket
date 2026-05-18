from pydantic import BaseModel


class BalanceResponse(BaseModel):
    free_balance: float
