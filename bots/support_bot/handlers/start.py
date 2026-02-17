from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from backend.bots_backend.roles import is_admin, is_ceo
from ..keyboards.user_inline import user_start_menu
from ..keyboards.admins_inline import admins_start_menu

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext):
    await state.clear()
    user_id = message.from_user.id
    if is_admin(user_id):
        if is_ceo(user_id):
            await message.answer(
                "От лица кого вы хотите войти?",
                reply_markup=CEO_choice_menu()
            )
            return
        await message.answer(
            "Здравствуйте! Выберите раздел:",
            reply_markup=admin_choice_menu(),
        )
        return
    await message.answer(
        "Здравствуйте! Выберите раздел вашего вопроса, или перейдите к своим активным диалогам::",
        reply_markup=user_start_menu(),
    )

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

@router.callback_query(lambda c: c.data.startswith("choice:"))
async def get_dialog(callback: CallbackQuery):
    """Обработчик выбора"""
    key = callback.data.split(":")[1]
    if key == "user":
        await callback.message.edit_text(
            "хай",
            reply_markup=user_start_menu()
        )
        await callback.answer()
        return
    elif key == "admin":
        await callback.message.edit_text(
            "хай",
            reply_markup=admins_start_menu()
        )
        await callback.answer()
        return
    elif key == "CEO":
        await callback.message.edit_text(
            "Новый текст сообщения",
            reply_markup=admins_start_menu()
        )
        await callback.answer()
