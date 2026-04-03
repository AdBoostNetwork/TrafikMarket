import requests

from backend.config import tgstat_token
from backend.app_backend.app_classes import Chart, TgStatChannel, TgStatAd, ChannelPost
from backend.logger import get_logger


logger = get_logger(__name__)

base_api_url = "https://api.tgstat.ru/channels"


class ChartsData:
    endpoints = ("subscribers", "views", "avg-posts-reach", "er", "err", "err24")

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


def get_channel_info(params):
    url = f"{base_api_url}/get"

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        payload = response.json()
    except Exception as e:
        logger.error("Ошибка получения channel info с TgStat | error=%s", str(e))
        raise ValueError("Ошибка получения channel info с TgStat") from e

    if payload.get("status") != "ok":
        raise ValueError("Ошибка при получении данных")

    return payload["response"]


def get_channel_stat(params):
    url = f"{base_api_url}/stat"

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        payload = response.json()
    except Exception as e:
        logger.error("Ошибка получения channel stat с TgStat | error=%s", str(e))
        raise ValueError("Ошибка получения channel stat с TgStat") from e

    if payload.get("status") != "ok":
        raise ValueError("Ошибка при получении данных")

    return payload["response"]


def get_channel(channel: str):
    params = {
        "token": tgstat_token,
        "channelId": channel,
    }

    channel_info = get_channel_info(params)
    channel_stat = get_channel_stat(params)

    return TgStatChannel(
        title=channel_info["title"],
        topic=channel_info["category"],
        country=channel_info["country"],
        subs_count=channel_stat["participants_count"],
        cover_count=channel_stat["avg_post_reach"],
    )


def get_ad(channel: str):
    params = {
        "token": tgstat_token,
        "channelId": channel,
    }

    channel_info = get_channel_info(params)
    channel_stat = get_channel_stat(params)

    return TgStatAd(
        title=channel_info["title"],
        topic=channel_info["category"],
        country=channel_info["country"],
        subs_count=channel_stat["participants_count"],
        cover_count=channel_stat["avg_post_reach"],
        er=channel_stat["er_percent"],
    )


def get_last_posts(channel: str, posts_count: int):
    url = f"{base_api_url}/posts"
    params = {
        "token": tgstat_token,
        "channelId": channel,
        "limit": posts_count,
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        payload = response.json()
    except Exception as e:
        logger.error("Ошибка получения постов канала с TgStat | error=%s", str(e))
        raise ValueError("Ошибка получения постов канала с TgStat") from e

    if payload.get("status") != "ok":
        raise ValueError("Ошибка при получении данных")

    posts_list = []
    for item in payload["response"]["items"]:
        posts_list.append(
            ChannelPost(
                text=item["text"],
                media=item["media"],
                views=item["views"],
            )
        )

    return posts_list