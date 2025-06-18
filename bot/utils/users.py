from aiogram.types import Message

from bot.schemas.user import User


def extract_user_data(message: Message) -> User:
    user_data = {
        "telegram_id": message.from_user.id,
        "username": message.from_user.username,
        "first_name": message.from_user.first_name if message.from_user.first_name else None
    }
    return User.model_validate(**user_data)
