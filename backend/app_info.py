#Файл с информацией о функциях для взаимодействия фронтенда с бэкендом

#Основная библиотека для связи фронтенда с бэкендом — FastAPI (https://fastapi.tiangolo.com/)
from fastapi import FastAPI

app = FastAPI()

# ==== Страница 1 (Главное меню) ====

"На этой странице фронтенду ничего не нужно от бэкенда."




# ==== Страница 2 (Меню объявлений: Каналы/Реклама/Трафик/Аккаунты) ====

# ==== Страница 2.1 (Меню объявлений: Каналы) ====

class SellerInfo:
    """
    Класс с данными продавца


    :param name — Имя продавца,
    :param deals_count — Количество сделок продавца,
    :param success_deals — Процент успешных сделок продавца
    """
    name: str
    deals_count: int
    success_deals: int


class AnnounInfo:
    """
    Класс, объект которого содержит информацию об одном объявлении для страницы

    :param seller — Объект класса SellerInfo,
    :param name — Название объявления,
    :param price — Цена объявления,
    :param short_description — Краткое описание объявления, отображающееся на странице,
    :param type_value — Значение категории объявления (пример, для канала — тематика и тд)
    """
    seller: SellerInfo
    name: str
    price: float
    short_description: str
    type_value: str


class AnnounsList:
    """
    Класс, объект которого содержит список объявлений

    :param announs: list[AnnounInfo]
    """
    announs: list[AnnounInfo]


class ChnsFilters:
    """
    Класс, который содержит набор фильтров для раздела "Каналы"

    :param topic — Тематика канала
    :param country — Страна
    :param chn_type — Тип (Открытый/Закрытый)

    :param price_from — Цена от
    :param price_to — Цена до

    :param subs_from — Подписчики от
    :param subs_to — Подписчики до

    :param profit_from — Доходность от
    :param profit_to — Доходность до

    :param cover_from — Охват от
    :param cover_to — Охват до

    :param requests_for_join — Заявки на вступление (Да/Нет)

    = None сделано для того, чтобы все параметры были необязательными (пользователь может не выбрать часть/все фильтры)
    """
    topic: str = None
    country: str = None
    chn_type: str = None
    price_from: int = None
    price_to: int = None
    subs_from: int = None
    subs_to: int = None
    profit_from: int = None
    profit_to: int = None
    cover_from: int = None
    cover_to: int = None
    requests_for_join: bool = None


@app.get("/get_channels_list")
#Ручка FastAPI, делающая get запрос к серверу для получения данных списка объявлений тематики "Каналы"

def get_channels_list(
        topic: str = None,
        country: str = None,
        chn_type: str = None,
        price_from: int = None,
        price_to: int = None,
        subs_from: int = None,
        subs_to: int = None,
        profit_from: int = None,
        profit_to: int = None,
        cover_from: int = None,
        cover_to: int = None,
        requests_for_join: bool = None):
        """
        Создаёт объект класса ChnsFilters и заполняет его полученными аргументами. После этого передаёт его в функицю БД, которая возвращает список объявлений.
        Аргументы пояснять не буду, тк они расписаны в классе ChnsFilters

        Что-то вроде:

        active_filters = ChnsFilters(params), где params — полученный список аргументов.
        get_channels_list_db(active_filters)

        :return AnnounsList
        """


def get_channels_list_db(active_filters: ChnsFilters):
    """
    Делает запрос к БД для получения списка объявлений каналов в соответсвтии с фильтрами. Заполняет ими объекты класса AnnounInfo и AnnounsList
    :param active_filters — Полученный набор фильтров

    :return: AnnounsList
    """


# ==== Страница 3 (Страница объявления) ====


class FullAnnounInfo:
    """
    Класс с данными объявления. Объект этого класса создаётся при запросе данных для заполнения объявления и содержит:

    :param seller — Объект класса SellerInfo, содержит Имя, количество сделок и процент успешных сделок продавца,
    :param title — Название объявления,
    :param price — Цена объявления,
    :param ...
    """
    seller: SellerInfo
    title: str
    price: float


@app.get("/get_announ")
#Ручка FastAPI, делающая get запрос к серверу для получения данных открытого объявления

def get_announ(announ_id: int):
    """
    Вызывает функцию БД для получения информации об объявлении по его announ_id
    Возврашает данные объявления в виде объекта класс FullAnnounInfo

    :param announ_id — Id объявления

    :return FullAnnounInfo
    """

def get_announ_info_db(announ_id: int):
    """
    Делает запрос к БД по announ_id и возвращает информацию в виде переменных

    :param announ_id — Id объявления

    :return: name, deals_count, success_deals, title, price, ...
    """




# ==== Страница 4 (Заказы) ====

class OrderInfo:
    """
    Класс, объект которого содержит информацию об одном заказе/объявлении для страницы "Заказы".
    Список из таких объектов составляет объект класса MyOrders, который передаётся странице.

    :param seller — Объект класса SellerInfo,
    :param name — Название заказа/объявления,
    :param price — Цена заказа/объявления,
    :param short_description — Краткое описание заказа/объявления, отображающееся на странице,
    :param type_value — Значение категории заказа/объявления (пример, для канала — тематика и тд)
    """
    seller: SellerInfo
    name: str
    price: float
    short_description: str
    type_value: str


class MyOrders:
    """
    Класс, объект которого состоит из списка объектов OrderInfo

    :param orders — Список объектов OrderInfo
    """
    orders: list[OrderInfo]


@app.get("/get_my_orders")
#Ручка FastAPI, делающая get запрос к серверу для получения данных о заказах пользователя
def get_my_orders(user_id: int, orders_type: str):
    """
    Вызывает функцию БД для получения данных о заказах для выбранного типа (Активные заказы; Завершённые заказы; Мои объявления)
    Возвращает данные в формате объекта класса MyOrders

    :param user_id — Id пользователя, обращающегося к приложению,
    :param orders_type — Тип страницы заказов. Может принимать одно из трёх значений

    1. active — Активные заказы пользователя
    2. closed — Завершённые заказы пользователя
    3. my_announs — Объявления, созданные пользователем

    :return: MyOrders
    """


def get_my_orders_db(user_id: int, orders_type: str):
    """
    Делает запрос к БД по user id и типу: active/closed
    Возвращает данные, которые позже родительская функция записывает в класс OrderInfo

    :param user_id — Id пользователя
    :param orders_type — Active/Closed

    :return
    """


def get_my_announs_db(user_id: int):
    """
    Делает запрос к БД по user id и возвращает активные объявления пользователя

    :param user_id — Id пользователя
    :return data — Данные объявлений
    """




# ==== Страница 5 (Реферальные ссылки) ====

@app.get("/ref_link")
#Ручка FastAPI, делающая get запрос к серверу для получения реферальной ссылки пользователя

def get_ref_link(user_id: int):
    """
    Вызывает функцию БД (get_ref_link_db) для получения реферальной ссылки пользователя по user_id
    Возвращает ссылку (строку)

    :param user_id — Id пользователя, который обращается к приложению
    :return: ref_link — Строка с ссылкой
    """


def get_ref_link_db(user_id: int):
    """
    Делает запрос к БД для получения реферальной ссылки по user_id

    :param user_id — Id пользователя
    :return: ref_link — Строка с ссылкой
    """




# ==== Страница 6 (Профиль) ====

class MyProfile:
    """
    Класс с данными профиля. Объект этого класса создаётся при запросе данных для страницы профиля и заполняется данными:

    :param name — Имя пользователя,
    :param deals_count — Количество сделок пользователя,
    :param success_deals — Процент успешных сделок пользователя,
    :param balance — Текущий баланс пользователя,
    :param deps_list — Список пополнений и списаний пользователя
    """
    name: str
    deals_count: int
    success_deals: int
    balance: float
    deps_list: list


@app.get("/my_profile")
#Ручка FastAPI, делающая get запрос к серверу для получения данных, нужных для отрисовки страницы профиля

def get_profile(user_id: int):
    """
    Вызывает функцию БД (get_profile_info_db) для получения данных профиля по user_id, заполняет ими объект класса MyProfile и возвращает его.

    :param user_id — Id пользователя, который обращается к приложению
    :return: MyProfile
    """

def get_profile_info_db(user_id: int):
    """
    Делает запрос к БД для получения данных профиля по user_id и возвращает их в виде набора переменных:
    (name, deals_count, success_deals, balance, deps_list)

    :param user_id — Id пользователя
    :return: name, deals_count, success_deals, balance, deps_list
    """




# ==== Страница 7 (Создание объявления) ====