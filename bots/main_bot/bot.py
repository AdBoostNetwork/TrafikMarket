import asyncio
from aiogram import Bot, Dispatcher

from .config import BOT_TOKEN
from .handlers import start, user_callbacks, user_market_callbacks, admin_callbacks, question

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(start.router)
    dp.include_router(user_callbacks.router)
    dp.include_router(admin_callbacks.router)
    dp.include_router(question.router)
    dp.include_router(user_market_callbacks.router)

    await dp.start_polling(bot)

def run():
    asyncio.run(main())

if __name__ == '__main__':
    run()