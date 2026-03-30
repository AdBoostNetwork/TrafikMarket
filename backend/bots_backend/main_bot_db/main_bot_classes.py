from dataclasses import dataclass



"""Классы для ответов на кнопки из /start"""
@dataclass(frozen=True)
class Wallet:
    """ Данные для раздела кошелька в боте"""
    active_ballance: float
    frozen_ballance: float




"""Классы для раздела маркета"""
@dataclass(frozen=True)
class AnnounsList:
    """ Объявления для n-ной страницы в боте. Содержит конфиги кнопок для объявлений с 10*(n-1)
     по 10*n-1.Также содержит n (current_index) и индекс максимально возможной страницы (max_index)
     (Не ласт странице может быть менее 10 значений)"""
    announs_list: set #{"Announ_name - price$": announ_id}
    max_index: int
    current_index: int


@dataclass(frozen=True)
class AnnounOfChannel:
    """Данные объявления по продаже канала"""
    article: int
    title: str
    seller_id: int
    short_about: str
    long_about: str
    channel_link: str
    channel_topic: str
    country: str
    subs_number: int
    coverage: int
    profitability: int
    applications: bool
    authorial: bool
    channel_cost: float

@dataclass(frozen=True)
class AnnounOfAd:
    """Данные объявления по рекламе"""
    article: int
    title: str
    seller_id: int
    short_about: str
    long_about: str
    channel_link: str
    country: str
    subs_number: int
    coverage: int
    cpm: int
    er: int
    ad_format: set

    
    #все, что есть в объявлении

@dataclass(frozen=True)
class AnnounOfTraff:
    """Данные объявления по траффику"""
    article: int
    title: str
    seller_id: int
    short_about: str
    long_about: str
    platform: str
    traff_type: str
    audience_type: str
    country: str
    sub_cost: float



#TODO: тут нужны классы для откликов и их списка

@dataclass(frozen=True)
class MyDealsList:
    """Список сделок пользователя, формат, аналогичный формату списка объявлений"""
    deals_list: set  # {"Покупка/продажа/отклик deal_name: deal_id}
    max_index: int
    current_index: int

@dataclass(frozen=True)
class MyDeal:
    """Класс для конкретной сделки"""
    #все, что есть в сделке


@dataclass(frozen=True)
class ChatsList:
    """ Xfns для n-ной страницы в боте. Содержит конфиги кнопок для чатов с 10*(n-1)
         по 10*n-1. Также содержит n (current_index) и индекс максимально возможной страницы (max_index)
         (Не ласт странице может быть менее 10 значений)"""
    chats_list: set  # {"Чат с user_to_name": chat_id}
    max_index: int
    current_index: int

@dataclass(frozen=True)
class Chat:
    """Класс для конкретного чата"""
    



