from aiogram.types import TelegramObject
from dishka import Provider, Scope, provide
from dishka.integrations.aiogram import AiogramMiddlewareData

from bot.services.users import AuthUser

class AuthProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_auth_service(self, event: TelegramObject, middleware_data: AiogramMiddlewareData) -> AuthUser:
        return AuthUser()
