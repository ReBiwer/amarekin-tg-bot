from logging import Logger
from dishka import FromDishka
from aiogram.dispatcher.router import Router
from aiogram import F
from aiogram.types import Message

from bot.services.ai_service import AIService
from bot.utils.ai import extract_user_query

router = Router()

@router.message(F.text)
async def text_user(
        message: Message,
        ai_service: FromDishka[AIService],
        logger: FromDishka[Logger]
):
    user_query = extract_user_query(message)
    logger.debug(f"Получили запрос пользователя: {user_query.model_dump()}")
    result = await ai_service.send_query_to_ai(user_query)
    logger.debug(f"Полученный ответ от ИИ: {result.model_dump()}")
    await message.answer(result.response)
