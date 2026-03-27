import requests

from .config import tgstat_token
from .logger import get_logger


logger = get_logger(__name__)

base_api_url = "https://api.tgstat.ru/channels"


def get_channel_info(channel: str):
    url = f"{base_api_url}/stat"
    params = {
        "token": tgstat_token,
        "channelId": channel,
    }
    response = requests.get(url, params=params)

    ...


def get_last_posts(channel: str, posts_count: int):
    url = f"{base_api_url}/posts"
    params = {
        "token": tgstat_token,
        "channelId": channel,
    }
    ...


def get_charts(channel: str):
    ...