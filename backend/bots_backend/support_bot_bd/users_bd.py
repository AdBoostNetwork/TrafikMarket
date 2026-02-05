def create_new_appeal (user_id, topic):
    """
    Создает новую апелляцию, файл для чата, и папку для доп файлов.
    Возвращает id обращения
    :param user_id:
    :param topic:
    :return:
    """


def can_user_make_appeal(user_id):
    """
    Проверяет, что у данного пользователя меньше пяти активных диалогов,
    если это так, возвращает True, в ином случае возвращает False
    :param user_id:
    :return: bool
    """
    return True


def msg_to_support(appeal_id: int, text: str, filenames: list):
    """
    получает Appeal_chat() по appeal_id, добавляет text к Appeal_chat.chat и ставит его Appeal_chat.last_msg,
    заменяет Appeal_chat.last_msg_files на filenames, ставит ставит Appeal_chat.status=waiting_adm

    :param appeal_id:
    :param text:
    :param filenames:
    :return:
    """


def download_file(appeal_id: int, file):
    """
    Сохранение приложенного файла. Вызывается столько раз, сколько файлов приложено. Избежать конфликта имен. Возвращает имя.
    :param appeal_id:
    :param file:
    :return: filename
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