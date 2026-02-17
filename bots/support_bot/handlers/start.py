from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from backend.bots_backend.roles import is_admin
from ..keyboards.user_inline import user_start_menu
from ..keyboards.admins_inline import admins_start_menu

router = Router()


@router.message(CommandStart(), F.chat.type == "private")
async def start_handler(message: Message, state: FSMContext):
    await state.clear()
    user_id = message.from_user.id
    if is_admin(user_id):
        await message.answer(
            "Здравствуйте! Выберите раздел:",
            reply_markup=admins_start_menu(),
        )
        return
    await message.answer(
        "Здравствуйте! Выберите раздел вашего вопроса, или перейдите к своим активным диалогам::",
        reply_markup=user_start_menu(),
    )