from dishka import FromDishka
from aiogram.dispatcher.router import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from bot.services.users import AuthUser
from bot.utils.users import extract_user_data
from bot.config import settings

router = Router()

@router.message(CommandStart())
async def start(message: Message, auth_service: FromDishka[AuthUser]):
    user_data = extract_user_data(message)
    await auth_service.check_user(user_data)
    await message.answer(settings.START_MESSAGE)
