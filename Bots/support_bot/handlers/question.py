from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from ..states.support import SupportState
from Backend.bot_func import msg_to_support

router = Router()

@router.message(SupportState.waiting_for_question)
async def handle_question(message: Message, state: FSMContext):
    user_id = message.from_user.id
    text = message.text

    msg_to_support(user_id=user_id, text=text)

    await message.answer(
        "Ваш вопрос успешно отправлен, дожидайтесь ответа"
    )

    await state.clear()