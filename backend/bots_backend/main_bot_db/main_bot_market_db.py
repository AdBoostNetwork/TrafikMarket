from .main_bot_classes import (AnnounsList, AnnounOfAd, AnnounOfTraff, AnnounOfChannel, ResponsesList)



"""Рездел маркета"""


"""__________________________________________________"""

"""Действия с объявлениями"""

async def create_announ_db(create_announ_scheme) -> bool:
    """Определяет класс полученной переменной и создает нужное объявление

    :param create_announ_scheme: схема для создания объявления:
    :return: успешность действия"""
    return True

async def get_announs_list_db(filters, current_index = 0) -> AnnounsList:
    """Определяет класс полученного фильтра, и возвращает n-ную страницу списка объявлений по фильтру"""
    return AnnounsList(
        announs_list={
            "Канал 'Горячие киски' - 300$": 12345,
            "rats  - 100$": 1,
            "cats - 100$": 123,
            "dogs - 100$": 1234
        },
        max_index=9,
        current_index=3
    )

async def get_user_announs_list_db(user_id, current_index = 0) -> AnnounsList:
    """
    Возвращает n-ную страницу списка объявлений пользователя
    :param user_id: id пользователя
    :param current_index: n
    :return:
    """
    return AnnounsList(
        announs_list={
            "Канал 'Горячие киски' - 300$": 12345,
            "rats  - 100$": 1,
            "cats - 100$": 123,
            "dogs - 100$": 1234
        },
        max_index=9,
        current_index=3
    )

async def get_announ_db(announ_id):
    """
    Возвращает данные объявления по айди/артикулу
    :param announ_id: ???
    :return:
    """
    return AnnounOfChannel(
        article=1234,
        title="Sell BDC channel",
        seller_id=12345,
        seller_name="4epTujla",
        seller_deals_number=100,
        seller_scs_deals_percent=95,
        short_about="I wanna to sell channel about black big dicks",
        long_about="I wanna to sell channel about black big dicks",
        channel_link="https://www.youtube.com/c/BDC",
        channel_topic="BDC",
        country="Russia",
        subs_number=10000,
        coverage=300,
        profitability=300,
        applications=False,
        authorial=False,
        channel_cost=800.8
    )





"""__________________________________________________"""


"""Действия с откликами"""


async def get_responses_list_db(article: int) -> ResponsesList:
    """
    Возвращает конфиг для кнопок для выбора отклика на объявление(на страницах по 10 откликов,
    на ласт странице может быть меньше)


    :param article: артикул объявления
    """
    return ResponsesList()

async def get_response_db(response_id):
    """
    Возвращает данные для принятия/отклонения отклика по айди

    :param response_id: айдишка отклика
    """

async def accept_response_db(response_id, user_from_id):
    """
    Проверяет, что объявление, на которое оставлен отклик было создал пользователь user_from_id,
    и, если это так, создает сделку на основе сделки и отклика.
    Возвращает успешность действия, и айди сделки.

    :param response_id:
    :param user_from_id:
    """
    return True, 1234

async def cancel_response_db(response_id, user_from_id) -> bool:
    """
    Проверяет, что отклик создан user_from_id или сделка, на которую оставили отклик создана user_from_id,
    и, если это так, отменяет отклик. Возвращает успешность действия

    :param response_id:
    :param user_from_id:
    """
    return True