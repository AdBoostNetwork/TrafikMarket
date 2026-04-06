import requests

from backend.config import tgstat_token
from backend.app_backend.app_classes import Chart, TgStatChannel, TgStatAd, ChannelPost
from backend.logger import get_logger


logger = get_logger(__name__)

base_api_url = "https://api.tgstat.ru/channels"


class ChartsData:
    endpoints = ("subscribers", "views", "avg-posts-reach", "er", "err", "err24")
    current_value_map = {
        "subscribers": "participants_count",
        "views": "daily_reach",
        "avg-posts-reach": "avg_post_reach",
        "er": "er_percent",
        "err": "err_percent",
        "err24": "err24_percent",
    }

    def __init__(self, channel: str):
        self.channel = channel
        self.params = {
            "token": tgstat_token,
            "channelId": self.channel
        }
        self.channel_stat = get_channel_stat(self.params)

    @staticmethod
    def count_metrics(items: list[dict]):
        if not items:
            return None, None, None

        def format_delta(delta):
            formatted = f"{delta:+.2f}".rstrip("0").rstrip(".")
            return "0" if formatted in ("+0", "-0") else formatted

        metric_key = next(key for key in items[0] if key != "period")
        current = items[0][metric_key]

        yesterday_value = format_delta(current - items[1][metric_key]) if len(items) > 1 else None
        week_value = format_delta(current - items[7][metric_key]) if len(items) > 7 else None
        month_value = None

        return yesterday_value, week_value, month_value

    def get_chart_data(self, endpoint: str):
        url = f"{base_api_url}/{endpoint}"

        try:
            response = requests.get(url, params=self.params, timeout=10)
            response.raise_for_status()
            payload = response.json()

            if payload.get("status") != "ok":
                raise ValueError(f"Ошибка при получении данных")

            items = payload["response"]
            yesterday_value, week_value, month_value = self.count_metrics(items)
            current_value = self.channel_stat[self.current_value_map[endpoint]]

            return Chart(
                title=endpoint,
                points=items,
                current_value=current_value,
                yesterday_value=yesterday_value,
                week_value=week_value,
                month_value=month_value,
            )

        except Exception as e:
            logger.error("Ошибка запроса TGStat | endpoint=%s | error=%s", endpoint, str(e))
            raise ValueError("Ошибка HTTP-запроса к TGStat") from e

    def get_charts_data(self):
        charts_list = []

        for endpoint in self.endpoints:
            charts_list.append(self.get_chart_data(endpoint))
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