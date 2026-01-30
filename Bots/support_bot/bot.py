import asyncio
from aiogram import Bot, Dispatcher

from .config import BOT_TOKEN
from .handlers import start, callbacks, question

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(start.router)
    dp.include_router(callbacks.router)
    dp.include_router(question.router)

    await dp.start_polling(bot)

def run():
    asyncio.run(main())

if __name__ == '__main__':
    run()