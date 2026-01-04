def msg_to_support(user_id, text):
    """получает appeal() по user_id, если нет, то создает, добавляет text к appeal.chat, ставит appeal.status=response_waiting
    :param user_id:
    :param text:
    """