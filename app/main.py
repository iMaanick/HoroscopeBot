import asyncio
import os

from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.types import BotCommand
from dotenv import load_dotenv

from app.dialogs import setup_all_dialogs
from app.handlers import setup_handlers, setup_unknown_text
from app.middlewares import setup_middlewares
from app.models import create_pool


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="start"),
        BotCommand(command="/update", description="update"),
        BotCommand(command="/change_zodiac", description="change_zodiac"),
        BotCommand(command="/clear_history", description="clear_history"),

    ]
    await bot.set_my_commands(commands)


async def main():
    load_dotenv()
    token = os.getenv('TOKEN')
    if not token:
        raise ValueError("TOKEN env variable is not set")

    dp = Dispatcher()
    await setup_middlewares(dp, create_pool())
    setup_handlers(dp)
    setup_all_dialogs(dp)
    setup_unknown_text(dp)

    bot = Bot(
        token=token,
        default=DefaultBotProperties(parse_mode='HTML')
    )
    await set_commands(bot)
    print("started")

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
