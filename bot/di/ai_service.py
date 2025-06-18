from dishka import Provider, Scope, provide

from bot.services.ai_service import AIService

class AIProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_ai_service(self) -> AIService:
        return AIService()
