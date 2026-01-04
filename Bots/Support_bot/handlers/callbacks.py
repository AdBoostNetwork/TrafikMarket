from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from ..states.support import SupportState

router = Router()

SECTION_NAMES = {
    "finance": "Финансы",
    "orders": "Заказы",
    "moderation": "Модерация объявлений",
}

@router.callback_query(lambda c: c.data.startswith("support:"))
async def support_section(callback: CallbackQuery, state: FSMContext):
    section_key = callback.data.split(":")[1]
    section_name = SECTION_NAMES.get(section_key, "выбранному разделу")

    await state.set_state(SupportState.waiting_for_question)
    await state.update_data(section=section_name)

    await callback.message.answer(
        f"Задайте свой вопрос по разделу «{section_name}»"
    )

    await callback.answer()