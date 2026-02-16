from sqlalchemy import text

from .db_engine import new_session
from ..logger import get_logger


logger = get_logger(__name__)

