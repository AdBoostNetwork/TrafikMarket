import asyncio
from .main_bot_classes import Wallet, AnnounsList

""" Раздел кошелька"""
async def get_wallet_info(user_id) -> Wallet:
    """
    Получает информацию о балике юзера, для кнопки "Кошелек"
    :param user_id:
    :return:
    """
    return Wallet(active_ballance=100, frozen_ballance=100)


"""Рездел маркета"""
async def get_announs_list() -> AnnounsList:
    """Получает список объявлений для траницы"""
    #TODO: бсудить как быть с обновлением списка и фильтрами
    return AnnounsList()

async def get_my_announs_list(user_id, current_index = 0) -> AnnounsList:
    """
    Возвращает n-ную страницу списка объявлений пользователя
    :param user_id: id пользователя
    :param current_index: nf.
    :return:
    """
    return AnnounsList()

async def get_announ(announ_id):
    """
    Возвращает данные объявления по айди/артикулу
    :param announ_id: ???
    :return:
    """
    return 