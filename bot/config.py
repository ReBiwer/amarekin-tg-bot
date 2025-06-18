from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    TELEGRAM_BOT_TOKEN: SecretStr = "YOUR_TELEGRAM_BOT_TOKEN"
    BACKEND_URL: str = "http://localhost:8080"
    NAME_LOGGER: str = "tg_bot"

    model_config = SettingsConfigDict(env_file=f"/{BASE_DIR}/.env", extra="ignore")


settings = Settings()
