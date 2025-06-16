import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager, AbstractAsyncContextManager

from backend.api.v1.endpoints import users, ai
from backend.di import init_di_web
from backend.core.log_settings import setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI) -> AbstractAsyncContextManager[None]:
    setup_logging()
    init_di_web(app)
    yield
    await app.state.dishka_container.close()

app = FastAPI(
    title="Telegram AI Assistant Backend",
    description="Backend for handling AI requests from Telegram bot."
)

app.include_router(ai.router)
app.include_router(users.router)


def create_app() -> FastAPI:
    app = FastAPI(
        title="Telegram AI Assistant Backend",
        description="Backend for handling AI requests from Telegram bot.",
        lifespan=lifespan,
    )
    return app


if __name__ == "__main__":
    uvicorn.run("web:create_app", port=8000, factory=True, reload=True)
