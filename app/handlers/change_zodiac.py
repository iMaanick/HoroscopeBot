from aiogram import Dispatcher, Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode, ShowMode

from app.states import Register


async def change_zodiac_cmd(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(Register.choose_zodiac, mode=StartMode.RESET_STACK, show_mode=ShowMode.DELETE_AND_SEND)


def setup_change_zodiac(dp: Dispatcher):
    router = Router(name=__name__)
    router.message.register(change_zodiac_cmd, Command("change_zodiac"))

    dp.include_router(router)
