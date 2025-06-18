from logging import Logger
from dishka import FromDishka
from aiogram.dispatcher.router import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from bot.services.users import AuthUser
from bot.utils.users import extract_user_data
from bot.config import settings

router = Router()

@router.message(CommandStart())
async def start(
        message: Message,
        auth_service: FromDishka[AuthUser],
        logger: FromDishka[Logger],
):
    user_data = extract_user_data(message)
    logger.debug(f"Старт диалога для пользователя: {user_data.model_dump()}")
    result = await auth_service.check_user(user_data)
    logger.debug(f"Результат отправки данных на бек: {result}")
    await message.answer(settings.START_MESSAGE)
