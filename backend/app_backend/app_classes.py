#Классы app
from dataclasses import dataclass
from pydantic import BaseModel


@dataclass(frozen=True)
class AppDbConfig:
    """Класс конфигурации данных БД основного приложения"""
    admin: str
    password: str
    host: str
    port: int
    db_name: str


@dataclass(frozen=True)
class FastApiConfig:
    """Класс конфигурации хоста и порта основного приложения"""
    host: str
    port: int


@dataclass(frozen=True)
class Transaction:
    """История транзакций пользователя (тип, сумма, дата совершения)"""
    trn_type: str
    trn_summ: str
    trn_date: str


@dataclass(frozen=True)
class MyProfile:
    """Класс с данными для страницы профиля"""
    name: str
    avatar_filename: str
    deals_count: int
    success_deals_percent: int
    free_balance: float
    free_balance_rub: float
    rating: float
    deals_summ: float

    deps_list: list[Transaction]


@dataclass(frozen=True)
class RefSchema:
    """Список рефералов"""
    name: str
    avatar_filename: str
    vip_status: int
    deals_summ: float
    profit: float


@dataclass(frozen=True)
class RefAnswerSchema:
    """Ответ ручки реферальной страницы"""
    ref_link: str
    refs_list: list[RefSchema]


@dataclass(frozen=True)
class AnnounPageSchema:
    """Ответ единой страницы объявления"""
    type: str
    announ_info: object


@dataclass(frozen=True)
class SellerInfo:
    """Класс с данными продавца"""
    name: str
    deals_count: int
    success_deals_percent: int
    rating: float


@dataclass(frozen=True)
class ClosedAnnoun:
    """Класс с данными объявления на странице просмотра объявлений"""
    announ_id: int
    seller: SellerInfo
    title: str
    price: float
    description: str
    topic: str


@dataclass(frozen=True)
class CommonFilters:
    """Класс общих фильтров"""
    topic: str
    country: str
    min_price: float
    max_price: float


@dataclass(frozen=True)
class ChannelsFilters(CommonFilters):
    """Класс фильтров Каналов"""
    min_subs_count: int
    max_subs_count: int
    type: str
    min_cover: float
    max_cover: float
    min_profit: float
    max_profit: float
    on_requests: bool
    author: bool


@dataclass(frozen=True)
class AdFilters(CommonFilters):
    """Класс фильтров Рекламы"""
    min_subs_count: int
    max_subs_count: int
    min_cover: float
    max_cover: float
    min_cpm: float
    max_cpm: float
    min_er: float
    max_er: float


@dataclass(frozen=True)
class TrafficFilters(CommonFilters):
    """Класс фильтров Трафика"""
    platform: str
    traffic_type: str
    audience_type: str
    min_leads: int
    max_leads: int


@dataclass(frozen=True)
class OpenedAnnoun:
    """Класс общих параметров открытого объявления"""
    article: int
    seller: SellerInfo
    title: str
    description: str
    imgs: list[str]


@dataclass(frozen=True)
class ChannelSchema(OpenedAnnoun):
    """Класс параметров объявления тематики Каналы"""
    channel_link: str
    price: float
    topic: str
    chn_type: str
    country: str
    subs_count: int
    cover_count: float
    profit: float
    on_requests: bool
    author: bool


@dataclass(frozen=True)
class AdSchema(OpenedAnnoun):
    """Класс параметров объявления тематики Реклама"""
    channel_link: str
    prices: dict[str, float]
    topic: str
    country: str
    subs_count: int
    cover: int
    cpm: int
    er: int


@dataclass(frozen=True)
class TrafficSchema(OpenedAnnoun):
    """Класс параметров объявления тематики Трафик"""
    topic: str
    platform: str
    traffic_type: str
    audience_type: str
    country: str
    min_leads: int
    max_leads: int
    price: float


class AnnounCreateSchema(BaseModel):
    """Схема структуры ответа ручки получения объявления"""
    type: str
    announ_info: dict


@dataclass(frozen=True)
class Chart:
    """Структура данных графика"""
    title: str
    current_value: str
    yesterday_value: str | None
    week_value: str | None
    month_value: str | None
    data: list[dict]


@dataclass(frozen=True)
class TgStatChannel:
    """Класс данных канала, получаемых с TgStat"""
    title: str
    topic: str
    country: str
    subs_count: int
    cover_count: float


@dataclass(frozen=True)
class TgStatAd(TgStatChannel):
    """Класс данных рекламы, получаемых с TgStat"""
    er: float


@dataclass(frozen=True)
class ChannelPost:
    """Класс данных поста"""
    text: str | None
    media: str | None
    views: int


@dataclass(frozen=True)
class TopicsConfig:
    """Класс конфигурации списка тематик, стран, типов аудитории и платформ"""
    topics: list[str]
    countries: list[str]
    audience_types: list[str]
    platforms: list[str]


@dataclass(frozen=True)
class OtherProfile:
    """Класс с данными для страницы профиля другого пользователя"""
    name: str
    avatar_filename: str
    rating: float
    deals_count: int
    success_deals_percent: int
    deals_summ: float
    registration_date: str
    was_online: str