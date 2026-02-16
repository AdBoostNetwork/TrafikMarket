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
    frozen_balance: float
    deps_list: list[Transaction]


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
class AnnounBaseSchema:
    """Класс с общими данными объявления для всех типов объявлений"""
    seller: SellerInfo
    title: str
    price: int
    long_text: str
    imgs: list[str]


@dataclass(frozen=True)
class ChannelSchema(AnnounBaseSchema):
    """Класс параметров объявления тематики Каналы"""
    topic: str
    chn_type: str
    country: str
    subs_count: int
    cover_count: float
    profit: float


@dataclass(frozen=True)
class AdSchema(AnnounBaseSchema):
    """Класс параметров объявления тематики Реклама"""
    topic: str
    country: str
    cover: int
    cpm: int
    er: int

@dataclass(frozen=True)
class TrafficSchema(AnnounBaseSchema):
    """Класс параметров объявления тематики Трафик"""
    topic: str
    platform: str
    traffic_type: str
    audience_type: str
    country: str


@dataclass(frozen=True)
class AccSchema(AnnounBaseSchema):
    """Класс параметров объявления тематики Аккаунты"""
    country: str
    log_type: str
    idle_time: str
    acc_type: str
    premium: str
    stars_count: str
    gifts: bool
    tg_level: int


class AnnounCreateSchema(BaseModel):
    type: str
    announ_info: dict