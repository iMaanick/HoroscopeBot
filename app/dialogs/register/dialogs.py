import operator

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Select, Group
from aiogram_dialog.widgets.markup.reply_keyboard import ReplyKeyboardFactory
from aiogram_dialog.widgets.text import Const, Format

from app.dialogs.register.getters import get_zodiac_buttons
from app.dialogs.register.handlers import on_zodiac_sign_selected
from app.dialogs.utils import unknown_message_input
from app.states import Register

register_dialog = Dialog(
    Window(
        Const("Выбери знак зодиака"),
        Group(
            Select(
                Format("{item[0]}"),
                id="zodiac_choose",
                items="zodiac_buttons",
                item_id_getter=operator.itemgetter(1),
                on_click=on_zodiac_sign_selected
            ),
            width=4
        ),
        unknown_message_input,
        markup_factory=ReplyKeyboardFactory(
            resize_keyboard=True,
        ),
        getter=get_zodiac_buttons,
        state=Register.choose_zodiac
    )
)
