from sqlalchemy import text

from backend.db_engine import new_session
from backend.logger import get_logger


logger = get_logger(__name__)


async def get_user_info_db(user_id: int):
    ...