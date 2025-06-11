from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    TELEGRAM_BOT_TOKEN: SecretStr = "YOUR_TELEGRAM_BOT_TOKEN"
    BACKEND_URL: str = "http://localhost:8000"
    DATABASE_URL: str = "sqlite:///./sql_app.db"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings() 