import datetime
import operator
import os
import pprint

import typing
from aiogram import F, Bot
from aiogram.enums import ContentType
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button, SwitchTo, Cancel, Select, Group
from aiogram_dialog.widgets.markup.reply_keyboard import ReplyKeyboardFactory
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Const, Jinja, Multi, Format
from aiogram import html

from app.dao.holder import HolderDao
from app.dialogs.register.dialogs import unknown_message_input
from app.models import dto
from app.states import Horoscope


async def get_zodiac_name(dialog_manager: DialogManager) -> str:
    if "zodiac_name" in dialog_manager.dialog_data:
        return dialog_manager.dialog_data.get("zodiac_name")

    if dialog_manager.start_data and "zodiac_name" in dialog_manager.start_data:
        return dialog_manager.start_data.get("zodiac_name")

    dao: HolderDao = dialog_manager.middleware_data["dao"]
    user = await dao.user.get_by_tg_id(dialog_manager.event.from_user.id)
    return user.zodiac_sign


async def get_horoscope_by_zodiac_name(zodiac_name: str):
    current_date = datetime.datetime.now()
    return f"Horoscope for {zodiac_name} for the date {html.bold(current_date)}"


async def get_choose_zodiac(dialog_manager: DialogManager, **kwargs):
    zodiac_name = await get_zodiac_name(dialog_manager)

    if zodiac_name not in dialog_manager.dialog_data:
        dialog_manager.dialog_data["zodiac_name"] = zodiac_name

    horoscope = await get_horoscope_by_zodiac_name(zodiac_name)
    return {
        "horoscope": horoscope
    }


src_dir = os.path.normpath(os.path.join(__file__, os.path.pardir))

horoscope_dialog = Dialog(
    Window(
        Format("{horoscope}"),
        StaticMedia(
            path=os.path.join(src_dir, "./images/zodiac.jpg"),
            type=ContentType.PHOTO,
        ),
        SwitchTo(Const("Обновить"), id="get_horoscope_to_get_horoscope", state=Horoscope.get_horoscope),
        unknown_message_input,
        getter=get_choose_zodiac,
        state=Horoscope.get_horoscope
    )
)
