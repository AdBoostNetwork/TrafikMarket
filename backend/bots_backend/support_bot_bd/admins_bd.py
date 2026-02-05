def take_appeal(appeal_id):
    """
    Возвращает все, кроме статуса (расписывать не буду)

    :param appeal_id:
    :return:
    """

def msg_from_support(user_id, text):
    """
    Добавляет text к appeal.chat, ставит appeal.status=waiting_user
    :param user_id:
    :param text:
    :return:
    """


def config_tp_bot_buttons(user_id: int = None, status: str = None, circle: int = 0):
    """
    Ставит фильтр (идин из первых двух параметров, и из полученных значений БД делает срез [5*circle: 5*(circle+1)] тут обработать крайние значения).
    И возвращает словарь:
    config = {f"Обращение №{id} по теме {topic}": id
    f"Обращение №{id} по теме {topic}": id
    f"Обращение №{id} по теме {topic}": id
    f"Обращение №{id} по теме {topic}": id
    f"Обращение №{id} по теме {topic}": id
    }
    и булевcкое значение is_end

    :param user_id:
    :param status:
    :param circle:
    :return: config, is_end
    """

def close_appeal(appeal_id):
    """
    Закрывает апелляцию

    :param appeal_id:
    :return:
    """
