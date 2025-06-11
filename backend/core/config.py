from pathlib import Path
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    BACKEND_URL: str = "http://localhost:8000"
    OPENAI_API_KEY: SecretStr = ""
    DATABASE_URL: str = "sqlite:///./sql_app.db"
    PROXY_URL: str = "socks5h://127.0.0.1:1080"
    NAME_LOGGER: str = "backend"
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_NAME: str
    CONTAINER_DB_NAME: str

    model_config = SettingsConfigDict(env_file=f"/{BASE_DIR}/.env", extra="ignore")

    @property
    def db_url(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:5432/{self.DB_NAME}"



settings = Settings()
