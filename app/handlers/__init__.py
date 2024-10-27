import logging

from aiogram import Dispatcher

from app.handlers.change_zodiac import setup_change_zodiac
from app.handlers.clear_history import setup_clear_history
from app.handlers.start import setup_start
from app.handlers.unknown_text import setup_unknown_text
from app.handlers.update import setup_update


def setup_handlers(dp: Dispatcher):
    setup_start(dp)
    setup_update(dp)
    setup_change_zodiac(dp)
    setup_clear_history(dp)