from aiogram import Dispatcher
from dishka.integrations.aiogram import (
    AiogramProvider,
    setup_dishka,
)
from dishka import make_async_container, AsyncContainer

from bot.di.auth import AuthProvider
from bot.di.logger_di import LoggerProvider


def container_factory() -> AsyncContainer:
    return make_async_container(
        AiogramProvider(), # для получения объектов AiogramMiddlewareData и TelegramObject в провайдерах
        AuthProvider(),
        LoggerProvider()
    )

def init_di_bot(dp: Dispatcher) -> None:
    container = container_factory()
    setup_dishka(container, router=dp, auto_inject=True)
