from aiogram import Dispatcher, Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode, ShowMode

from app.states import Register, Horoscope


async def update_cmd(message: Message, dialog_manager: DialogManager) -> None:
    await dialog_manager.start(Horoscope.get_horoscope, mode=StartMode.RESET_STACK, show_mode=ShowMode.DELETE_AND_SEND)


def setup_update(dp: Dispatcher) -> None:
    router = Router(name=__name__)
    router.message.register(update_cmd, Command("update"))

    dp.include_router(router)
