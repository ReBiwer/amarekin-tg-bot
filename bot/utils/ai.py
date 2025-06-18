from aiogram.types import Message

from bot.schemas.message import UserQuery

def extract_user_query(message: Message) -> UserQuery:
    data = {
        "query": message.text,
        "user_id": message.from_user.id,
        "chat_id": message.chat.id
    }
    return UserQuery.model_validate(data)
