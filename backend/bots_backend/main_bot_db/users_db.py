
async def get_profile_db(user_id: int) -> dict:
    """
    Вернуть то же, что возвращаем при использовании ручки страницы профиля. Объяснить мне формат
    :param user_id:
    :return:

    """


async def config_user_announs_buttons_db(user_id: int, circle: int) -> {dict, bool}:
    """
    Ставит фильтр (айди продавца или покупателя должно совпадать с user_id,и статус должен быть активного объявление),
    и из полученных значений БД делает срез [5*circle: 5*(circle+1)] (тут обработать крайние значения).
    Возвращает словарь:
    config = {
    f"{Announ.short_text}": id,
    f"{Announ.short_text}": id,
    f"{Announ.short_text}": id,
    f"{Announ.short_text}": id,
    f"{Announ.short_text}": id
    }
    И булевскую величину is_end, которая принимает истинное значение, когда мы берем ласт сделку юзера
    :param user_id:
    :return: config, is_end
    """
    return {
        "Вопрос по разделу 'Вывод'": 1234
    }

async def get_announ_db(announ_id: int):
    """
    Аналогично профилю, можно скопировать ручку.
    :param announ_id:
    :return:
    """

async def stop_announ_db(user_id: int, announ_id: int):
    """
    Для безопасности проверяем, что Announ.seller_id == user_id,
    а потом можно опять же скопировать ручку
    :param user_id:
    :param announ_id:
    :return:
    """


async def config_user_deals_buttons_db(user_id: int, circle: int) -> {dict, bool}:
    """
    Ставит фильтр (айди продавца или покупателя должно совпадать с user_id,и статус должен быть активной сделки),
    и из полученных значений БД делает срез [5*circle: 5*(circle+1)] (тут обработать крайние значения).
    Возвращает словарь:
    config = {
    f"{deal.deal_info}": id,
    f"{deal.deal_info}": id,
    f"{deal.deal_info}": id,
    f"{deal.deal_info}": id,
    f"{deal.deal_info}": id
    }
    И булевскую величину is_end, которая принимает истинное значение, когда мы берем ласт сделку юзера
    :param user_id:
    :return: config, is_end
    """
    return {
        "Вопрос по разделу 'Вывод'": 1234
    }

