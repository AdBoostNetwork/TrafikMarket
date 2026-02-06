#Классы app
from dataclasses import dataclass


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
    """Класс с данными профиля"""
    name: str
    deals_count: int
    success_deals: int
    balance: float
    deps_list: list[Transaction]