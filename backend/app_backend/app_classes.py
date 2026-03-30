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


@dataclass(frozen=True)
class ClosedAnnoun:
    """Класс с данными объявления на странице просмотра объявлений"""
    announ_id: int
    seller: SellerInfo
    title: str
    price: float
    description: str
    imgs: list[str]


@dataclass(frozen=True)
class OpenedAnnoun:
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
    price: float


class AnnounCreateSchema(BaseModel):
    type: str
    announ_info: dict


@dataclass(frozen=True)
class Chart:
    title: str
    data: list[dict]


@dataclass(frozen=True)
class TgStatChannel:
    title: str
    topic: str
    country: str
    subs_count: int
    cover_count: float


@dataclass(frozen=True)
class ChannelPost:
    text: str | None
    media: str | None
    views: int