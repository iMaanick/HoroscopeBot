from aiogram import Router

from .dialogs import register_dialog


def setup_register(router: Router):
    router.include_router(register_dialog)