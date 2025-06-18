from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    TELEGRAM_BOT_TOKEN: SecretStr = "YOUR_TELEGRAM_BOT_TOKEN"
    BACKEND_URL: str = "http://localhost:8080"
    NAME_LOGGER: str = "tg_bot"
    START_MESSAGE: str = """
        Привет! Это бот СемьСов: Семейные советы.\n\n
        
        Он создан для родителей, у которых есть вопросы. 
        Мы собираем базу данных статей и материалов экспертов в вопросах родительства и 
        ответы нашего бота - это не просто поиск по всему интернету - это выдача именно из 
        проверенных эксперных материалов.\n\n
        
        Просто задайте свой вопрос в свободной форме, например: "как выбрать беговел ребенку?", 
        "я не покупаю ребенку дорогие игрушки, но каждый раз, когда он приходит от бабушки, 
        он приносит с собой новый дорогой подарок. Мне это не нравится. Что делать?"
    """

    model_config = SettingsConfigDict(env_file=f"/{BASE_DIR}/.env", extra="ignore")


settings = Settings()
