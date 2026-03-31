from dataclasses import dataclass

"""Классы для функционирования бота"""

"________________________________"


"""Единичные классы"""
@dataclass(frozen=True)
class Wallet:
    """ Данные для раздела кошелька в боте"""
    active_balance: float
    frozen_balance: float


"_______________________________"

"""Классы для фильтров"""

#TODO: заполнить класссы
@dataclass(frozen=True)
class ChannelsFilters:
    """Класс фильтров под каналы"""
    smth: str

@dataclass(frozen=True)
class AdFilters:
    """Класс фильтров под рекламу"""
    smth: str

@dataclass(frozen=True)
class TraffFilters:
    """Класс фильтров под фильтры"""
    smth: str



"_______________________________"


"""Классы объявлений"""

@dataclass(frozen=True)
class CreateChannelAnnounScheme:
    """Класс для создания объявлений по каналам"""
    smth: str

@dataclass(frozen=True)
class CreateAdAnnounScheme:
    """Класс для создания объявлений по рекламе"""
    smth: str

@dataclass(frozen=True)
class CreateTraffAnnounScheme:
    """Класс для создания объявлений по траффику"""
    smth: str

@dataclass(frozen=True)
class AnnounsList:
    """ Объявления для n-ной страницы в боте. Содержит конфиги кнопок для объявлений с 10*(n-1)
     по 10*n-1. Также содержит n (current_index) и индекс максимально возможной страницы (max_index)
     (Не ласт странице может быть менее 10 значений)"""
    announs_list: dict #{"Announ_name - price$": announ_id}
    max_index: int
    current_index: int

@dataclass(frozen=True)
class AnnounOfChannel:
    """Данные объявления по продаже канала"""
    article: int
    title: str
    seller_id: int
    seller_name: str
    seller_deals_number: int
    seller_scs_deals_percent: float
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
    ad_format: dict


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


"_______________________"

"""Классы для откликов"""
@dataclass(frozen=True)
class ResponsesList:
    """Список откликов на объявление"""
    responses_list: dict #{"User_from_name - cost$": response_id}
    max_index: int
    current_index: int


@dataclass(frozen=True)
class ResponseToChannel:
    """Класс для передачи информации об отдельном отклике на продажу канала"""
    response_id: int
    user_from_name: str
    user_from_deals_number: int
    user_from_scs_deals_percent: float
    cost: float

@dataclass(frozen=True)
class ResponseToAd:
    """Класс для передачи информации об отдельном отклике на рекламу"""
    response_id: int
    user_from_name: str
    user_from_deals_number: int
    user_from_scs_deals_percent: float
    format: str
    cost: float

@dataclass(frozen=True)
class ResponseToTraff:
    """Класс для передачи информации об отдельном отклике на траффик"""
    response_id: int
    user_from_name: str
    user_from_deals_number: int
    user_from_scs_deals_percent: float
    sub_number: int
    cost: float


"______________________"

"""Классы для сделок"""

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


"______________________"

"""Классы для чатов"""

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
    



