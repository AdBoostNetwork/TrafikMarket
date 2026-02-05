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
async def create_new_dialog(callback: CallbackQuery, state: FSMContext):
    user_id = callback.message.from_user.id
    if not can_user_make_dialog(user_id):
        await callback.message.answer("Вы достигли максимального количества обращений в ТП. Чтобы создать новое обращение, закончите диалог по одному из предыдущих"
                                      "Чтобы это сделать, следуйте инструкции:\n"
                                      "/start -> 'Мои активные диалоги💬' -> Выберете одно из ваших обращений -> 'Закончить диалог🔴'")
        await callback.answer()
        return None

    create
    section_key = callback.data.split(":")[1]
    section_name = MAIN_MENU_SECTIONS.get(section_key)

    await state.set_state(SupportState.waiting_for_question)
    await state.update_data(section=section_name)

    await callback.message.answer(
        f"Задайте свой вопрос по разделу «{section_name}»"
    )

    await callback.answer()


@router.callback_query(lambda c: c.data.startswith("support:"))



@router.callback_query(lambda c: c.data.startswith("support:"))