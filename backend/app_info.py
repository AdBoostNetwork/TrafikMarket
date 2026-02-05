#Файл с информацией о функциях для взаимодействия фронтенда с бэкендом

#Основная библиотека для связи фронтенда с бэкендом — FastAPI (https://fastapi.tiangolo.com/)
from fastapi import FastAPI

app = FastAPI()

# ==== Страница 1 (Главное меню) ====

"На этой странице фронтенду ничего не нужно от бэкенда."




# ==== Страница 2 (Меню объявлений: Каналы/Реклама/Трафик/Аккаунты) ====


class FiltersInfo:
    ...

class AnnounsList:
    ...



@app.get("/get_announs_list")
#Ручка FastAPI, делающая get запрос к серверу для получения данных списка объявлений

def get_announs_list(announs_type: str):
    """
    Вызывает функцию БД для получения списка объявлений, а так же функцию БД для получения списка фильтров.
    Возвращает данные для страницы в формате объекта класса AnnounsList, содержащего информацию о фильтрах и объявлениях.

    :param announs_type - Тип объявлений (Каналы/Реклама/Трафик/Аккаунты). Принимает одно из значений.

    1. channels
    2. ads
    3. traffik
    4. accounts

    :return AnnounsList
    """




# ==== Страница 3 (Страница объявления) ====

class SellerInfo:
    """
    Класс с данными продавца. Объект этого класса создаётся при запросе данных для заполнения объявления и содержит:

    :param name — Имя продавца,
    :param deals_count — Количество сделок продавца,
    :param success_deals — Процент успешных сделок продавца
    """
    name: str
    deals_count: int
    success_deals: int


class AnnounInfo:
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
    Возврашает данные объявления в виде объекта класс AnnounInfo

    :param announ_id — Id объявления

    :return AnnounInfo
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

    :param seller — Объект класса SellerInfo (пояснение и структуру класса см выше, в описании страницы "Страница объявления"),
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