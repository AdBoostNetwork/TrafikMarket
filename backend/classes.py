from dataclasses import dataclass
import datetime


@dataclass(frozen=True)
class DbConfig:
    """Класс конфигурации данных БД"""
    admin: str
    password: str
    host: str
    port: int
    db_name: str


@dataclass(frozen=True)
class UserCreateSchema:
    """Класс данных пользователя при создании аккаунта"""
    user_id: int
    name: str
    registration_date: datetime.date
    avatar_id: int | None
    ref_link: str
    referi_id: int | None