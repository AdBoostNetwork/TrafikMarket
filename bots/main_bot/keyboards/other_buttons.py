from aiogram.types import MenuButtonWebApp, WebAppInfo


def user_mini_app_button():
    return MenuButtonWebApp(
        text="Nigga",
        web_app=WebAppInfo(url="https://pornhub.com")
    )