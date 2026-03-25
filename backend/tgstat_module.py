from .config import tgstat_token
from .logger import get_logger


logger = get_logger(__name__)


def get_channel_info(channel: str):
    ...


def get_last_posts(channel: str, posts_count: int):
    ...


def get_charts(channel: str):
    ...