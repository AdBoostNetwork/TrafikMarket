from dataclasses import dataclass

@dataclass(frozen=True)
class Wallet:
    """ Данные для раздела кошелька в боте"""
    active_ballance: float
    frozen_ballance: float


@dataclass(frozen=True)
class Announs_list:
    """ Объявления для n-ной страницы в боте. Содержит конфиги кнопок для объявлений с 10*(n-1)
     по 10*n-1.Также содержит n (current_index) и индекс максимально возможной страницы (max_index)
     (Не ласт странице может быть менее 10 значений)"""
    announs_list: set #{"Announ_name - price$": announ_id}
    max_index: int
    current_index: int


@dataclass(frozen=True)
class Chats_list:
    """ Xfns для n-ной страницы в боте. Содержит конфиги кнопок для чатов с 10*(n-1)
         по 10*n-1.Также содержит n (current_index) и индекс максимально возможной страницы (max_index)
         (Не ласт странице может быть менее 10 значений)"""
    chats_list: set  # {"Чат с user_to_name": chat_id}
    max_index: int
    current_index: int

