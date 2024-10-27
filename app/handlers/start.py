import pprint

from aiogram import Dispatcher, Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode, ShowMode

from app.dao.holder import HolderDao
from app.states import Register


async def start_cmd(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(Register.choose_zodiac, mode=StartMode.RESET_STACK, show_mode=ShowMode.DELETE_AND_SEND)


def setup_start(dp: Dispatcher):
    router = Router(name=__name__)
    router.message.register(start_cmd, Command("start"))

    dp.include_router(router)
