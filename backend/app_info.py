#Файл с информацией о функциях для взаимодействия фронтенда с бэкендом

#Основная библиотека для связи фронтенда с бэкендом — FastAPI (https://fastapi.tiangolo.com/)
from fastapi import FastAPI

app = FastAPI()

# ==== Страница 1 (Главное меню) ====

"На этой странице фронтенду ничего не нужно от бэкенда."




# ==== Страница 2 (Меню объявлений: Каналы/Реклама/Трафик/Аккаунты) ====

# ==== Страница 2.1 (Меню объявлений: Каналы)

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
        requests_for_join: bool = None
):
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
    Делает запрос к БД для получения списка объявлений каналов в соответствии с фильтрами. Заполняет ими объекты класса AnnounInfo и AnnounsList
    :param active_filters — Полученный набор фильтров

    :return: AnnounsList
    """




# ==== Страница 2.2 (Меню объявлений: Реклама)

class AdFilters:
    """
    Класс, который содержит набор фильтров для раздела "Реклама"

    :param topic — Тематика рекламы
    :param country — Страна

    :param cover_from — Охват от
    :param cover_to — Охват до

    :param cpm_from — ЦПМ от
    :param cpm_to — ЦПМ до

    :param er_from — ЕР от
    :param er_to — ЕР до

    :param price_from — Цена от
    :param price_to — Цена до
    """
    topic: str = None
    country: str = None
    cover_from: int = None
    cover_to: int = None
    cpm_from: int = None
    cpm_to: int = None
    er_from: int = None
    er_to: int = None
    price_from: int = None
    price_to: int = None


@app.get("/get_ad_list")
#Ручка FastAPI, делающая get запрос к серверу для получения данных списка объявлений тематики "Реклама"


def get_ad_list(
    topic: str = None,
    country: str = None,
    cover_from: int = None,
    cover_to: int = None,
    cpm_from: int = None,
    cpm_to: int = None,
    er_from: int = None,
    er_to: int = None,
    price_from: int = None,
    price_to: int = None
):
    """
    Создаёт объект класса AdFilters и заполняет его полученными аргументами. После этого передаёт его в функицю БД, которая возвращает список объявлений.
    Аргументы пояснять не буду, тк они расписаны в классе AdFilters

    active_filters = AdFilters(params), где params — полученный список аргументов.
    get_ad_list_db(active_filters)

    :return AnnounsList
    """


def get_ad_list_db(active_filters: AdFilters):
    """
    Делает запрос к БД для получения списка объявлений каналов в соответствии с фильтрами. Заполняет ими объекты класса AnnounInfo и AnnounsList
    :param active_filters — Полученный набор фильтров

    :return: AnnounsList
    """



# ==== Страница 2.3 (Меню объявлений: Трафик)

class TrafficFilters:
    """
    Класс, который содержит набор фильтров для раздела "Трафик"

    :param topic — Тематика
    :param platform — Платформа
    :param traffic_type — Тип залива
    :param audience_type — Тип аудитории
    :param country — Страна

    :param price_from — Цена от
    :param price_to — Цена до
    """
    topic: str = None
    platform: str = None
    traffic_type: str = None
    audience_type: str = None
    country: str = None
    price_from: int = None
    price_to: int = None


@app.get("/get_traffic_list")
#Ручка FastAPI, делающая get запрос к серверу для получения данных списка объявлений тематики "Трафик"


def get_traffic_list(
        topic: str = None,
        platform: str = None,
        traffic_type: str = None,
        audience_type: str = None,
        country: str = None,
        price_from: int = None,
        price_to: int = None
):
        """
        Создаёт объект класса TrafficFilters и заполняет его полученными аргументами. После этого передаёт его в функицю БД, которая возвращает список объявлений.
        Аргументы пояснять не буду, тк они расписаны в классе TrafficFilters

        active_filters = TrafficFilters(params), где params — полученный список аргументов.
        get_ad_list_db(active_filters)

        :return AnnounsList
        """


def get_traffic_list_db(active_filters: TrafficFilters):
    """
    Делает запрос к БД для получения списка объявлений каналов в соответствии с фильтрами. Заполняет ими объекты класса AnnounInfo и AnnounsList
    :param active_filters — Полученный набор фильтров

    :return: AnnounsList
    """




# ==== Страница 2.4 (Меню объявлений: Аккаунты)

class AccsFilters:
    """
    Класс, который содержит набор фильтров для раздела "Аккаунты"

    :param country — Страна
    :param log_type — Тип входа
    :param idle_time — Время отлеги
    :param acc_type — Тип (Траст/Новорег)
    :param premium — Премиум (нет/месяц/год/2 года)
    :param stars_count — Количество звезд
    :param gifts — Подарки (Да/Нет)
    :param tg_level — Уровень тг
    """
    country: str = None
    log_type: str = None
    idle_time: str = None
    acc_type: str = None
    premium: str = None
    stars_count: str = None
    gifts: bool = None
    tg_level: int = None


@app.get("/get_accs_list")
#Ручка FastAPI, делающая get запрос к серверу для получения данных списка объявлений тематики "Аккаунты"


def get_accs_list(
    country: str = None,
    log_type: str = None,
    idle_time: str = None,
    acc_type: str = None,
    premium: str = None,
    stars_count: str = None,
    gifts: bool = None,
    tg_level: int = None
):
    """
    Создаёт объект класса AccsFilters и заполняет его полученными аргументами. После этого передаёт его в функицю БД, которая возвращает список объявлений.
    Аргументы пояснять не буду, тк они расписаны в классе AccsFilters

    active_filters = AccsFilters(params), где params — полученный список аргументов.
    get_ad_list_db(active_filters)

    :return AnnounsList
    """

def get_accs_list_db(active_filters: AccsFilters):
    """
    Делает запрос к БД для получения списка объявлений каналов в соответствии с фильтрами. Заполняет ими объекты класса AnnounInfo и AnnounsList
    :param active_filters — Полученный набор фильтров

    :return: AnnounsList
    """




# ==== Страница 3 (Страница объявления) ====

class AnnounBaseSchema:
    """
    Класс с общими данными объявления для всех типов объявлений. Объект этого класса создаётся при запросе данных для заполнения объявления и содержит:

    :param seller — Объект класса SellerInfo, содержит Имя, количество сделок и процент успешных сделок продавца,
    :param title — Название объявления,
    :param price — Цена объявления,
    :param short_text — Краткое описание объявления,
    :param long_text — Подробное описание объявления,
    :param imgs — Картинки объявления
    """
    seller: SellerInfo
    title: str
    price: int
    short_text: str
    long_text: str
    imgs: list[str]




# ==== Страница 3.1 (Страница объявления: Каналы)

class ChannelSchema(AnnounBaseSchema):
    """
    Класс параметров объявления тематики "Каналы"

    :param topic — Тематика
    :param chn_type — Тип канала
    :param country — Страна
    :param subs_count — Количество подписичков
    :param cover_count — Охват
    :param profit — Доходность
    """
    topic: str
    chn_type: str
    country: str
    subs_count: int
    cover_count: int
    profit: int


@app.get("/get_chn_announ")
#Ручка FastAPI, делающая get запрос к серверу для получения данных открытого объявления тематики "Каналы"


def get_chn_announ(announ_id: int):
    """
    Вызывает функцию БД для получения информации об объявлении по его announ_id. Заполняет полученными данными объект ChannelSchema
    Возврашает данные объявления в виде объекта класс ChannelSchema

    :param announ_id — Id объявления

    :return ChannelSchema
    """


def get_chn_announ_db(announ_id: int):
    """
    Делает запрос к БД по announ_id и возвращает информацию в виде data[]

    :param announ_id — Id объявления

    :return: ChannelSchema
    """




# ==== Страница 3.2 (Страница объявления: Реклама)

class AdSchema(AnnounBaseSchema):
    """
    Класс параметров объявления тематики "Реклама"

    :param topic — Тематика
    :param country — Страна
    :param cover — Охват
    :param cpm — ЦПМ
    :param er — ЕР
    """
    topic: str
    country: str
    cover: int
    cpm: int
    er: int


@app.get("/get_ad_announ")
#Ручка FastAPI, делающая get запрос к серверу для получения данных открытого объявления тематики "Реклама"


def get_ad_announ(announ_id: int):
    """
    Вызывает функцию БД для получения информации об объявлении по его announ_id. Заполняет полученными данными объект AdSchema
    Возврашает данные объявления в виде объекта класс AdSchema

    :param announ_id — Id объявления

    :return AdSchema
    """


def get_ad_announ_db(announ_id: int):
    """
    Делает запрос к БД по announ_id и возвращает информацию в виде data[]

    :param announ_id — Id объявления

    :return: AdSchema
    """




# ==== Страница 3.3 (Страница объявления: Трафик)

class TrafficSchema(AnnounBaseSchema):
    """
    Класс параметров объявления тематики "Трафик"

    :param topic — Тематика
    :param platform — Платформа
    :param traffic_type — Тип залива
    :param audience_type — Тип аудитории
    :param country — Страна
    """
    topic: str
    platform: str
    traffic_type: str
    audience_type: str
    country: str


@app.get("/get_traffic_announ")
#Ручка FastAPI, делающая get запрос к серверу для получения данных открытого объявления тематики "Трафик"


def get_traffic_announ(announ_id: int):
    """
    Вызывает функцию БД для получения информации об объявлении по его announ_id. Заполняет полученными данными объект TrafficSchema
    Возврашает данные объявления в виде объекта класс TrafficSchema

    :param announ_id — Id объявления

    :return TrafficSchema
    """


def get_traffic_announ_db(announ_id: int):
    """
    Делает запрос к БД по announ_id и возвращает информацию в виде data[]

    :param announ_id — Id объявления

    :return: TrafficSchema
    """




# ==== Страница 3.4 (Страница объявления: Аккаунты)

class AccSchema(AnnounBaseSchema):
    """
    Класс параметров объявления тематики "Аккаунты"

    :param country — Страна
    :param log_type — Тип входа
    :param idle_time — Время отлеги
    :param acc_type — Тип (Траст/Новорег)
    :param premium — Премиум (нет/месяц/год/2 года)
    :param stars_count — Количество звезд
    :param gifts — Подарки (Да/Нет)
    :param tg_level — Уровень тг
    """
    country: str
    log_type: str
    idle_time: str
    acc_type: str
    premium: str
    stars_count: str
    gifts: bool
    tg_level: int


@app.get("/get_acc_announ")
#Ручка FastAPI, делающая get запрос к серверу для получения данных открытого объявления тематики "Аккаунты"


def get_acc_announ(announ_id: int):
    """
    Вызывает функцию БД для получения информации об объявлении по его announ_id. Заполняет полученными данными объект AccSchema
    Возврашает данные объявления в виде объекта класс AccSchema

    :param announ_id — Id объявления

    :return AccSchema
    """


def get_acc_announ_db(announ_id: int):
    """
    Делает запрос к БД по announ_id и возвращает информацию в виде data[]

    :param announ_id — Id объявления

    :return: AccSchema
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

class Transaction:
    """
    Класс с данными транзакций, нужными для отрисовки профиля

    :param trn_type — Тип транзакции, Пополнение/Списание
    :param trn_summ — Сумма транзакции
    :param trn_date — Дата и время транзакции
    """
    trn_type: str
    trn_summ: str
    trn_date: str


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
    deps_list: list[Transaction]


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

class AnnounCreateSchema:
    """
    Класс с общими данными объявления для создания всех типов объявлений

    :param seller_id — Id продавца
    :param status — Статус объявления
    :param title — Название объявления,
    :param price — Цена объявления,
    :param short_text — Краткое описание,
    :param long_text — Подробное описание,
    :param imgs — Картинки объявления
    """
    seller_id: int
    status: str
    title: str
    price: str
    short_text: str
    long_text: str
    imgs: list[str]


# ==== Страница 7.1 (Создание объявления Канала)

class ChannelCreateSchema(AnnounCreateSchema):
    """
    Класс параметров создания объявления тематики "Каналы".

    :param topic — Тематика,
    :param chn_type — Тип канала,
    :param country — Страна,
    :param subs_count — Количество подписчиков,
    :param cover_count — Охват,
    :param profit — Доходность
    """
    topic: str
    chn_type: str
    country: str
    subs_count: int
    cover_count: int
    profit: int


@app.post("/create_channel_announ")
#Ручка FastAPI, делающая post запрос к серверу для сохранения данных нового объявления Канала в БД


def create_channel_announ(data: ChannelCreateSchema):
    """
    Вызывает функцию БД для сохранения данных объявления

    :param data — Данные объявления

    :return: create_status — Успех или Ошибка, появляется из функции БД
    """


def create_channel_announ_db(data: ChannelCreateSchema):
    """
    Сохраняет данные объявления канала в БД

    :param data — Данные объявления

    :return: {"success": True}/{"error": error_value} — Возвращает либо успех, либо сообщение с ошибкой
    """




# ==== Страница 7.1 (Создание объявления Рекламы)

class AdCreateSchema(AnnounCreateSchema):
    """
    Класс параметров создания объявления тематики "Реклама"

    :param topic — Тематика
    :param country — Страна
    :param cover — Охват
    :param cpm — ЦПМ
    :param er — ЕР
    """
    topic: str
    country: str
    cover: int
    cpm: int
    er: int


@app.post("/create_ad_announ")
#Ручка FastAPI, делающая post запрос к серверу для сохранения данных нового объявления Рекламы в БД


def create_ad_announ(data: AdCreateSchema):
    """
    Вызывает функцию БД для сохранения данных объявления

    :param data — Данные объявления

    :return: create_status — Успех или Ошибка, появляется из функции БД
    """


def create_ad_announ_db(data: AdCreateSchema):
    """
    Сохраняет данные объявления канала в БД

    :param data — Данные объявления

    :return: {"success": True}/{"error": error_value} — Возвращает либо успех, либо сообщение с ошибкой
    """
