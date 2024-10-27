import operator
import pprint

import typing
from aiogram import F, Bot
from aiogram.enums import ContentType
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import Dialog, Window, DialogManager, StartMode, ShowMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, SwitchTo, Cancel, Select, Group
from aiogram_dialog.widgets.markup.reply_keyboard import ReplyKeyboardFactory
from aiogram_dialog.widgets.text import Const, Jinja, Multi, Format

from app.dao import UserDAO
from app.dao.holder import HolderDao
from app.states import Register, Horoscope
from app.models import dto

zodiac_signs = {
    "♈": "aries",
    "♉": "taurus",
    "♊": "gemini",
    "♋": "cancer",
    "♌": "leo",
    "♍": "virgo",
    "♎": "libra",
    "♏": "scorpio",
    "♐": "sagittarius",
    "♑": "capricorn",
    "♒": "aquarius",
    "♓": "pisces"
}

zodiac_descriptions = {
    "aries": "Aries: bold and ambitious, always ready for action.",
    "taurus": "Taurus: reliable and patient, grounded in practicality.",
    "gemini": "Gemini: adaptable and curious, loves learning and variety.",
    "cancer": "Cancer: sensitive and nurturing, values home and family.",
    "leo": "Leo: confident and charismatic, enjoys the spotlight.",
    "virgo": "Virgo: detail-oriented and analytical, always helping others.",
    "libra": "Libra: diplomatic and fair, seeks balance and harmony.",
    "scorpio": "Scorpio: passionate and intense, values honesty and loyalty.",
    "sagittarius": "Sagittarius: adventurous and optimistic, loves freedom.",
    "capricorn": "Capricorn: disciplined and hardworking, values stability.",
    "aquarius": "Aquarius: innovative and independent, thinks outside the box.",
    "pisces": "Pisces: compassionate and artistic, deeply in touch with emotions."
}


async def get_choose_zodiac(dialog_manager: DialogManager, **kwargs):
    zodiac = []
    for zodiac_emoji, zodiac_name in zodiac_signs.items():
        zodiac.append((zodiac_emoji, zodiac_name))

    return {
        "zodiac": zodiac
    }


async def on_zodiac_sign_selected(callback: CallbackQuery, widget: Select, manager: DialogManager,
                                  zodiac_name: str):
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


async def on_input_unknown(
        message: Message,
        widget: MessageInput,
        dialog_manager: DialogManager,
):
    bot_msg = await message.answer("Извините, я не понял")

    dao: HolderDao = dialog_manager.middleware_data["dao"]
    msg = dto.Message(message_id=bot_msg.message_id, chat_id=message.from_user.id)
    logged_message = await dao.message.insert_message(msg)

    await dao.commit()

    dialog_manager.show_mode = ShowMode.DELETE_AND_SEND


unknown_message_input = MessageInput(content_types=ContentType.ANY, func=on_input_unknown)

register_dialog = Dialog(
    Window(
        Const("Выбери знак зодиака"),
        Group(
            Select(
                Format("{item[0]}"),
                id="zodiac_choose",
                items="zodiac",
                item_id_getter=operator.itemgetter(1),
                on_click=on_zodiac_sign_selected
            ),
            width=4
        ),
        unknown_message_input,
        markup_factory=ReplyKeyboardFactory(
            resize_keyboard=True,
        ),
        getter=get_choose_zodiac,
        state=Register.choose_zodiac
    )
)
