from aiogram.enums import ContentType
from aiogram.types import Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import MessageInput

from app.dao.holder import HolderDao
from app.services.message import insert_message

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


async def on_input_unknown(
        message: Message,
        widget: MessageInput,
        dialog_manager: DialogManager,
):
    dao: HolderDao = dialog_manager.middleware_data["dao"]

    bot_msg = await message.answer("Извините, я не понял")

    await insert_message(bot_msg.message_id, message.from_user.id, dao)

    await dao.commit()

    dialog_manager.show_mode = ShowMode.DELETE_AND_SEND


unknown_message_input = MessageInput(content_types=ContentType.ANY, func=on_input_unknown)
