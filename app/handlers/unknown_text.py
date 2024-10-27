from aiogram import Dispatcher, Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode, ShowMode

from app.dao.holder import HolderDao
from app.dialogs.register.dialogs import zodiac_signs
from app.models import dto
from app.states import Register, Horoscope


async def unknown_text(message: Message, dialog_manager: DialogManager):
    bot_msg = await message.answer("Извините, я не понял")

    dao: HolderDao = dialog_manager.middleware_data["dao"]
    msg = dto.Message(message_id=bot_msg.message_id, chat_id=message.from_user.id)
    logged_message = await dao.message.insert_message(msg)
    await dao.commit()


def setup_unknown_text(dp: Dispatcher):
    router = Router(name=__name__)
    router.message.register(unknown_text, F.text.not_in(zodiac_signs))
    dp.include_router(router)
