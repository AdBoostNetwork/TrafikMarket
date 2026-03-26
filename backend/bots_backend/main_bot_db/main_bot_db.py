from sqlalchemy import text

from .main_bot_classes import Wallet, Announs_list, Announ
from backend.db_engine import new_session
from backend.logger import get_logger


logger = get_logger(__name__)


""" Раздел кошелька"""
async def get_wallet_info(user_id) -> Wallet:
    '''logger.info("Запрос баланса пользователя | user_id: %s", user_id)

    query = text("SELECT current_balance, frozen_balance FROM accounts WHERE user_id = :user_id")

    result = await new_session().execute(query, {"user_id": user_id})
    data = result.mappings().first()

    active_balance = float(data["current_balance"]) - float(data["frozen_balance"])

    return Wallet(
        active_ballance=active_balance,
        frozen_ballance=data["frozen_balance"]
    )'''

    return Wallet(active_balance=100, frozen_balance=100)


"""Рездел маркета"""
async def get_announs_list() -> Announs_list:
    """Получает список объявлений для траницы"""
    #TODO: бсудить как быть с обновлением списка и фильтрами
    return Announs_list()

async def get_my_announs_list(user_id, current_index = 0) -> Announs_list:
    """
    Возвращает n-ную страницу списка объявлений пользователя
    :param user_id: id пользователя
    :param current_index: n
    :return:
    """
    return Announs_list()

async def get_announ(announ_id) -> Announ:
    """
    Возвращает данные объявления по айди/артикулу
    :param announ_id: ???
    :return:
    """
    return Announ()