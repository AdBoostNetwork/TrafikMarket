from app.api.schemas.profile import BalanceResponse
from app.logger import get_logger
from app.repositories.profile import ProfileRepository

logger = get_logger(__name__)


class ProfileService:
    def __init__(self, repo: ProfileRepository) -> None:
        self._repo = repo

    async def get_balance(self, user_id: int) -> BalanceResponse:
        logger.info("Получение баланса | user_id=%s", user_id)
        row = await self._repo.get_balance(user_id)
        free_balance = float(row["current_balance"]) - float(row["frozen_balance"])
        return BalanceResponse(free_balance=free_balance)
