from aiogram import Dispatcher
from dishka.integrations.aiogram import (
    AiogramProvider,
    setup_dishka,
)
from dishka import make_async_container, Provider, provide, Scope, AsyncContainer

from bot.dialogs.start import router as start_router
from bot.di.auth import AuthProvider


def container_factory() -> AsyncContainer:
    return make_async_container(
        AiogramProvider(), # для получения объектов AiogramMiddlewareData и TelegramObject в провайдерах
        AuthProvider(),
    )

def init_di_bot(dp: Dispatcher) -> None:
    container = container_factory()
    setup_dishka(container, router=dp, auto_inject=True)
