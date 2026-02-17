def is_new_user_db(user_id: int) -> {bool, int}:
    """
     Проверяет есть ли юзер в БД, и возвращает сохраненный avatar_id
    :param user_id:
    :return:
    """
    return True, 1488


def save_new_user_db(user_id, name, tg_username, avatar_id) -> bool:
    """
    Сохраняет новый акк в БД, возвращает False в смлучае ошибки, True если все норм
    :param user_id:
    :param name:
    :param tg_username:
    :param avatar_id:
    :return:
    """
    return True
