from pydantic import BaseModel


class UserMessage(BaseModel):
    query: str
    user_id: int
    chat_id: int


class AIResponse(BaseModel):
    response: str
    chat_id: int
