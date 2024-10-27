from aiogram import Bot
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, StartMode, ShowMode
from aiogram_dialog.widgets.kbd import Select

from app.dao.holder import HolderDao
from app.dialogs.utils import zodiac_descriptions
from app.models import dto
from app.states import Horoscope


async def on_zodiac_sign_selected(
        callback: CallbackQuery,
        widget: Select,
        manager: DialogManager,
        zodiac_name: str
):
    bot: Bot = manager.middleware_data["bot"]
    dao: HolderDao = manager.middleware_data["dao"]
    user_dto = dto.User(tg_id=callback.from_user.id, zodiac_sign=zodiac_name, first_name=callback.from_user.first_name)
    await dao.user.upsert_user(user_dto)

    bot_msg = await bot.send_message(callback.from_user.id, zodiac_descriptions[zodiac_name])
    msg = dto.Message(message_id=bot_msg.message_id, chat_id=callback.from_user.id)
    logged_message = await dao.message.insert_message(msg)

    await dao.commit()

    await manager.start(
        Horoscope.get_horoscope,
        data=
        {
            'zodiac_name': zodiac_name
        },
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.DELETE_AND_SEND
    )
