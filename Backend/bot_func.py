from database import get_appeal_buy_id, change_appeal, create_appeal
from classes import Appeal


async def msg_to_support(user_id, text):
    appeal = await get_appeal_buy_id(user_id)

    if appeal == "appeal_not_found":
        new_appeal = Appeal(
            user_from_id=user_id,
            last_msg=text,
            chat=f"Сообщение пользователя: {text}",
            status="response_waiting",
        )
        return await create_appeal(new_appeal)

    return await change_appeal(
        user_from_id=user_id,
        status="response_waiting",
        last_msg=text,
        chat_append=f"Сообщение пользователя: {text}",
    )



async def msg_from_support(user_id, text):

    await change_appeal(
        user_from_id=user_id,
        status="closed",
        last_msg=text,
        chat_append=f"Сообщение админа: {text}")

    return