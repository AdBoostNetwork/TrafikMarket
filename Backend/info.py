class account():
    """аккаунт
    Хранится:
    1)id (tg id int)
    2)name (str max 50 smbols)
    3)current_balance (float)
    4)ids_of_deals (list of ints)
    5)scs_count (int)
    6)id_of_trnactions (list of ints)
    7)id_of_amnts (list of ints)
    8)ref_link (str max 50 smbols)
    9)ref_ids (list of ints)
    10)referi (int)
    11)is_banned (bool)


    Сoздается при нажатии /start в боте.
    """


class trnaction():
    """
    1) trnaction_id (int)
    2) status (finished/in_progress/canceled)
    3) trnactn_time (datetime)
    4) summ (float)
    5) sys_msg (str) #для сохранения типа ошибки, чтобы админы могли помочь
    """



class announ():
    """
    1) announ_id
    2) announ_name
    3) seller_id
    3) price
    4) topic
    5)
    """

class deal():
    """
    1) deal_id (int)
    2) announ_id (int)
    3) buyer_id (int)
    4) buyer_trnaction_id (int)
    5) seller_trnaction_id (int)
    6) type (str) (scs_completed/canceled/active)
    7) chat (str)
    """


def acc_maker(user_id, ref_id):
    """
    Создает новый аккаунт
    Порядок действий:
    1) Создает ник
    2) Создает реф ссылку
    3) остальное заполняет нулями/пустыми списками
    4) Сохраняет акк в БД

    :param user_id:
    :param ref_id:
    :return: account
    """

def get_account_info(user_id, ref_id = None):
    """
    Запускается при запуске бота. Если акка с таким id не существует, запускает функцию acc_maker

    :param user_id: tg_id (int)
    :param ref_id: refer_id (int)|None
    :return: account
    """

def dep(summ):
    """
    Создает платеж и, после ответа от криптобота, создает объект типа trnaction, зачисляет деньги на балик и присылает уведомление в боте
    :param summ:(float) сумма депа
    :return:
    """

def undep(summ):
    """
    Списывает деньги со счета, создает объект типа trnaction и выводит деньги через платежку

    Возможно, надо будет в аргументы добавить адрес кошеля
    :param summ:
    :return:
    """

