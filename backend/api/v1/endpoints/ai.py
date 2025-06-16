from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute

from fastapi import APIRouter
from backend.schemas.message import UserMessage, AIMessage
from backend.services.ai_service import AIService


router = APIRouter(
    prefix="/ai",
    tags=["ai_service"],
    route_class=DishkaRoute,
)


@router.post("/generate_response")
async def generate_response(user_message: UserMessage, ai_service: FromDishka[AIService]):
    ai_response_content = await ai_service.ainvoke_response(user_message.user_id, user_message.query)
    return AIMessage(response=ai_response_content, chat_id=user_message.chat_id)
