from httpx import AsyncClient

from bot.config import settings
from bot.schemas.message import UserMessage, AIResponse


class AIService:
    def __init__(self):
        self.client = AsyncClient()

    async def send_query_to_ai(self, user_message: UserMessage) -> AIResponse | None:
        response = await self.client.post(
            url=f"{settings.BACKEND_URL}/ai/generate_response",
            content=user_message.model_dump_json(),
        )
        if response.status_code == 200:
            return AIResponse.model_validate_json(response.content)
        # TODO если ответ не положительный, то райзить ошибку
