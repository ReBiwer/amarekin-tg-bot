from dishka import AsyncContainer, make_async_container
from dishka.integrations.fastapi import setup_dishka as fastapi_dishka
from fastapi import FastAPI

from backend.di.ai import AIProvider
from backend.di.user_dao import UserDAOProvider


def init_di_web(app: FastAPI) -> None:
    container = container_factory()
    fastapi_dishka(container, app)


def container_factory() -> AsyncContainer:
    return make_async_container(
        AIProvider(),
        UserDAOProvider()
    )
