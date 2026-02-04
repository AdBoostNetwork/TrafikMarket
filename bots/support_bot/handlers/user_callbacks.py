from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from ..states.support import SupportState

router = Router()

MAIN_MENU_SECTIONS = {
    "dep": "Пополнения",
    "undep": "Вывод",
    "announs": "Объявления",
    "deals": "Сделки",
    "acc": "Аккаунт",
    "other": "Другое  ",
}

@router.callback_query(lambda c: c.data.startswith("support:"))
async def support_section(callback: CallbackQuery, state: FSMContext):
    section_key = callback.data.split(":")[1]
    section_name = MAIN_MENU_SECTIONS.get(section_key, "выбранному разделу")

    await state.set_state(SupportState.waiting_for_question)
    await state.update_data(section=section_name)

    await callback.message.answer(
        f"Задайте свой вопрос по разделу «{section_name}»"
    )

    await callback.answer()