from multiprocessing import Process

from bots.support_bot.bot import run as sup_bot_run
from bots.main_bot.bot import run as main_bot_run
from backend.app_backend.app import app_run


if __name__ == "__main__":
    procs = [
        Process(target=sup_bot_run, name="support-bot"),
        Process(target=main_bot_run, name="main-bot"),
        Process(target=app_run, name="fastapi"),
    ]

    for p in procs:
        p.start()

    for p in procs:
        p.join()