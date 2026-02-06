from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from ..keyboards.user_inline import return_button
from ..states.support import SupportState
from backend.bots_backend.support_bot_db.users_db import msg_to_support
router = Router()

@router.message(SupportState.waiting_for_question)
async def handle_question(message: Message, state: FSMContext):
    data = await state.get_data()
    appeal_id = data["appeal_id"]
    text = message.text

    msg_to_support(appeal_id, text, "str")

    await message.answer(
        "Ваш вопрос успешно отправлен, дожидайтесь ответа",
        reply_markup=return_button()
    )

    await state.clear()