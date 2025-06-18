from pydantic import BaseModel


class UserQuery(BaseModel):
    query: str
    user_id: int
    chat_id: int


class AIResponse(BaseModel):
    response: str
    chat_id: int
