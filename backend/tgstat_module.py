import requests

from .config import tgstat_token
from backend.app_backend.app_classes import Chart, ChannelPost
from .logger import get_logger


logger = get_logger(__name__)

base_api_url = "https://api.tgstat.ru/channels"


class ChartsData:
    endpoints = ("subs", "views", "avg-posts-reach", "er", "err", "err24")

    def __init__(self, channel: str):
        self.channel = channel

    @staticmethod
    def get_chart_data(endpoint: str, params):
        url = f"{base_api_url}/{endpoint}"

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            payload = response.json()

            if payload.get("status") != "ok":
                raise ValueError(f"Ошибка при получении данных")

            return Chart(
                title=endpoint,
                data=payload["response"],
            )

        except Exception as e:
            logger.error("Ошибка запроса TGStat | endpoint=%s | error=%s", endpoint, str(e))
            raise ValueError("Ошибка HTTP-запроса к TGStat") from e

    def get_charts_data(self):
        params = {
            "token": tgstat_token,
            "channelId": self.channel
        }

        charts_list = []

        for endpoint in self.endpoints:
            charts_list.append(self.get_chart_data(endpoint, params))
        return charts_list


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
        "limit": posts_count,
    }

    posts_list = []

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        payload = response.json()

        if payload.get("status") != "ok":
            raise ValueError(f"Ошибка при получении данных")

        for item in payload["response"]["items"]:
            posts_list.append(
                ChannelPost(
                    text=item["text"],
                    media=item["media"],
                )
            )

        return posts_list
    except Exception as e:
        logger.error("Ошибка получения постов канала с TgStat | error: ", str(e))
        raise ValueError("Ошибка получения постов канала с TgStat") from e
