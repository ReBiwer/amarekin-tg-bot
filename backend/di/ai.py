from dishka import Provider, Scope, provide

from backend.services.ai_service import AIService

class AIProvider(Provider):
    scope = Scope.REQUEST

    ai_service = provide(AIService)
