import logging
from logging import Logger
from dishka import Provider, Scope, provide

from bot.config import settings


class LoggerProvider(Provider):
    @provide(scope=Scope.APP)
    def get_logger_app(self) -> Logger:
        logger = logging.getLogger(settings.NAME_LOGGER)
        return logger
