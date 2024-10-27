from aiogram import Dispatcher, Router
from aiogram_dialog import setup_dialogs

from app.dialogs.horoscope import setup_horoscope
from app.dialogs.register import setup_register


def setup_all_dialogs(dp: Dispatcher):
    dialog_router = Router()
    setup_register(dialog_router)
    setup_horoscope(dialog_router)
    dp.include_router(dialog_router)
    setup_dialogs(dp)