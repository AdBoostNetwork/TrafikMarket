from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton



def admin_choice_menu():
    """Только для админов, выбор от лица кого запускать бота"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Админ", callback_data="choice:admin"),
                InlineKeyboardButton(text="Юзер", callback_data="choice:user"),
            ],
        ]
    )

def CEO_choice_menu():
    """Только для админов, выбор от лица кого запускать бота"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="CEO", callback_data="choice:CEO"),
                InlineKeyboardButton(text="Юзер", callback_data="choice:user"),
            ],
        ]
    )

def admins_start_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Посмотреть вопросы пользователей", callback_data="adm_get_dialogs"),
            ],
            [
                InlineKeyboardButton(text="Ответить на самый старый вопрос", callback_data="get_latest_dialog"),
            ]
        ]
    )

def CEO_start_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Посмотреть споры по заказам", callback_data="adm_get_dialogs"),
            ],
            [
                InlineKeyboardButton(text="Ответить на самый старый вопрос", callback_data="get_latest_dialog"),
            ]
            [
                InlineKeyboardButton(text="Посмотреть список админов", callback_data="adm_list"),
            ],
            [
                InlineKeyboardButton(text="Добавить админа", callback_data="new_adm"),
            ],
        ]
    )

def admin_dialogs_list_menu(dialog_list, is_end: bool):
    """
        Меню с выбором активных диалогов
        :param dialog_list: конфигурационный словарь, ключ - название кнопки, значение - айди диалога
        :return:
        """
    menu = list(
        [InlineKeyboardButton(text=dialog_name, callback_data=f"adm_get_dialog:{dialog_list[dialog_name]}")] for dialog_name
        in dialog_list)
    if not is_end:
        menu.append([InlineKeyboardButton(text="Следующие 5 вопросов", callback_data="adm_get_dialog"), ])
    menu.append([InlineKeyboardButton(text="Вернуться🔙", callback_data="adm_return_to_start"), ])
    return InlineKeyboardMarkup(
        inline_keyboard=menu
    )

def admin_dialog_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="История диалога⏮️", callback_data="adm:get_history"),
                InlineKeyboardButton(text="Закончить диалог🔴", callback_data="adm:finish_dialog"),
            ],
            [
                InlineKeyboardButton(text="Ответить пользователю✍️", callback_data="adm:answer"),
            ]
        ]
    )

def adm_return_button():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Вернуться🔙", callback_data="adm_return_to_start"),
            ]
        ]
    )

