from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def user_start_menu():
    """
    Стартовая менюшка
    :return:
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Открыть биржу", url="pornhub.com"),
            ],
            [
                InlineKeyboardButton(text="Профиль👤", callback_data="profile"),
                InlineKeyboardButton(text="Поддержка", url = "pornhub.com"),
            ],
            [
                InlineKeyboardButton(text="Вывод⤴️", callback_data="finance:undep"),
                InlineKeyboardButton(text="Пополнение⤵️", callback_data="finance:undep"),
            ],
            [
                InlineKeyboardButton(text="Мои объявления 🗣", callback_data="my:announs"),
            ],
            [
                InlineKeyboardButton(text="Мои сделки 🤝", callback_data="my:deals"),
            ]
        ]
    )


def user_dialogs_list_menu(dialog_list):
    """
    Меню с выбором активных диалогов
    :param dialog_list: конфигурационный словарь, ключ - название кнопки, значение - айди диалога
    :return:
    """
    menu=list([InlineKeyboardButton(text=dialog_name, callback_data=f"get_dialog:{dialog_list[dialog_name]}")] for dialog_name in dialog_list)
    menu.append([InlineKeyboardButton(text="Вернуться🔙", callback_data="return_to_start"),])
    return InlineKeyboardMarkup(
        inline_keyboard=menu
    )


def user_announ_menu():
    """Меню для управления объявлением"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Посмотреть объявление", url="pornhub.com"),
            ],
            [
                InlineKeyboardButton(text="Закрыть объявление🔴", callback_data="announ:end"),
            ],
            [
                InlineKeyboardButton(text="Вернуться🔙", callback_data="return_to_start"),
            ]
        ]
    )

def user_deal_menu(is_buyer: bool):
    """Меню для управления сделкой"""
    if is_buyer:
        return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Посмотреть объявление", url="pornhub.com"),
            ],
            [
                InlineKeyboardButton(text="Чат сделки", callback_data="deal:chat"),
            ],
            [
                InlineKeyboardButton(text="Подтвердить выполнение", callback_data="deal:finish"),
            ],
            [
                InlineKeyboardButton(text="Вызвать поддержку", callback_data="deal:help"),
            ],
            [
                InlineKeyboardButton(text="Вернуться🔙", callback_data="return_to_start"),
            ]
        ]
    )
    else:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="Посмотреть объявление", url="pornhub.com"),
                ],
                [
                    InlineKeyboardButton(text="Чат сделки", callback_data="deal:chat"),
                ],
                [
                    InlineKeyboardButton(text="Вызвать поддержку", callback_data="deal:help"),
                ],
                [
                    InlineKeyboardButton(text="Вернуться🔙", callback_data="return_to_start"),
                ]
            ]
        )

def dialog_chat_menu():
    """Меню для чата сделки"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="История диалога⏮️", callback_data="deal_chat:history"),
            ],
            [
                InlineKeyboardButton(text="Ответить✍️", callback_data="deal:answer"),
            ],
            [
                InlineKeyboardButton(text="Вернуться🔙", callback_data="return_to_start"),
            ]
        ]
    )


def deal_help_confirm_menu():
    """Подтверждение вызова поддержки"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Да, вызвать поддержку", callback_data="deal:confirm_help"),
            ],
            [
                InlineKeyboardButton(text="Отмена", callback_data="return_to_start"),
            ]
        ]
    )

def deal_finish_confirm_menu():
    """Подтверждение выполнения заказа для покупателя"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Подтвердить выполнение", callback_data="deal:confirm_finish"),
            ],
            [
                InlineKeyboardButton(text="Отмена", callback_data="return_to_start"),
            ]
        ]
    )

def return_button():
    """ Тут даже огузок поймет"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Вернуться🔙", callback_data="return_to_start"),]
        ]
    )