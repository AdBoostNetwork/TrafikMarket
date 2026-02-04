from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def admins_start_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Посмотреть вопросы пользователей", callback_data="get_gialogs"),
            ]
        ]
    )

def admin_dialogs_list_menu(circle:int = 0):
    dialog_list=dict()# тут будет конфигурационная функция
    menu=list([InlineKeyboardButton(text=dialog_name, callback_data=f":{dialog_list(dialog_name)}"),] for dialog_name in dialog_list)
    menu.append([InlineKeyboardButton(text="Вернуться🔙", callback_data="return_to_start"),])
    return InlineKeyboardMarkup(
        inline_keyboard=menu
    )

def addmin_dialog_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Посмотреть историю диалога⏮️", callback_data="dialog:get_history"),
                InlineKeyboardButton(text="Закончить диалог🔴", callback_data="dialog:finish_dialog"),
            ],
            [
                InlineKeyboardButton(text="Продолжить диалог✍️", callback_data="dialog:answer"),
            ],
            [
                InlineKeyboardButton(text="Вернуться🔙", callback_data="return_to_start"),
            ]
        ]
    )

