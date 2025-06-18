from httpx import AsyncClient

from bot.config import settings
from bot.schemas.user import User


class AuthUser:
    """
    Данный класс должен создаваться для каждого пользователя отдельно и проверять его регистрацию на беке
    Если есть, то все ок и вернуть данные о нем. Если нет зарегистрировать
    """
    def __init__(self):
        self.client = AsyncClient()

    async def check_user(self, user: User):
        response = await self.client.post(
            url=f"{settings.BACKEND_URL}/users/telegram/add",
            content=user.model_dump_json()
        )
        return response.status_code == 200

