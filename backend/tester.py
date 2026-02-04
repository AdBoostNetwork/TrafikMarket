import asyncio

from .database import get_appeal_buy_id, create_appeal
from .classes import Appeal


new_appeal = Appeal(
    user_from_id=112,
    last_msg="message",
    chat="chat",
    status="response_waiting",
)

async def tester():
    result = await get_appeal_buy_id(111)
    print(result)

    #result = await change_appeal_status(111, "closed")
    #print(result)

    #result = await create_appeal(new_appeal)
    #print(result)

    #result = await get_appeal_buy_id(112)
    #print(result)

asyncio.run(tester())