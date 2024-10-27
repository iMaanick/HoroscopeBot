from aiogram.fsm.state import StatesGroup, State


class Register(StatesGroup):
    choose_zodiac = State()


class Horoscope(StatesGroup):
    get_horoscope = State()
