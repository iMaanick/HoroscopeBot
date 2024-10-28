from aiogram import Router

from .dialogs import horoscope_dialog


def setup_horoscope(router: Router) -> None:
    router.include_router(horoscope_dialog)