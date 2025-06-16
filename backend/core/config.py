from pathlib import Path
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    BACKEND_URL: str = "http://localhost:8080"
    LM_MODEL_NAME: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    PROXY_URL: str = "socks5h://127.0.0.1:1080"
    NAME_LOGGER: str = "backend"
    OPENAI_API_KEY: SecretStr
    SECRET_TOKEN_CHROMA: SecretStr
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_NAME: str
    CONTAINER_DB_NAME: str
    CONTAINER_CHROMA_NAME: str
    REDIS_HOST: str
    REDIS_PORT: str
    REDIS_DB: str


    model_config = SettingsConfigDict(env_file=f"/{BASE_DIR}/.env", extra="ignore")

    @property
    def db_url(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:5432/{self.DB_NAME}"

    @property
    def redis_url(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

settings = Settings()
