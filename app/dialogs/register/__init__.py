from aiogram import Router

from .dialogs import register_dialog


def setup_register(router: Router) -> None:
    router.include_router(register_dialog)