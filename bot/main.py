import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, BotCommandScopeDefault

from bot.config import settings
from bot.di import init_di_bot
from bot.dialogs import main_router
from bot.log_settings import setup_logging


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Старт"),
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())


async def main():
    bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
    await set_commands(bot)
    dp = Dispatcher()
    dp.include_router(main_router)
    init_di_bot(dp)
    setup_logging()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
