from aiogram import Dispatcher, Router, Bot
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode, ShowMode

from app.dao.holder import HolderDao
from app.states import Register, Horoscope


async def clear_history_cmd(message: Message, dialog_manager: DialogManager):

    dao: HolderDao = dialog_manager.middleware_data["dao"]
    message_ids = await dao.message.get_message_ids_by_chat_id(message.from_user.id)
    for message_id in message_ids:
        try:
            bot: Bot = dialog_manager.middleware_data["bot"]
            await bot.delete_message(message.from_user.id, message_id)
        except Exception as e:
            pass
    await dialog_manager.start(Horoscope.get_horoscope, mode=StartMode.RESET_STACK, show_mode=ShowMode.DELETE_AND_SEND)


def setup_clear_history(dp: Dispatcher):
    router = Router(name=__name__)
    router.message.register(clear_history_cmd, Command("clear_history"))

    dp.include_router(router)
