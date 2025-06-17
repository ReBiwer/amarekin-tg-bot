import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager, AbstractAsyncContextManager

from backend.api.v1.endpoints import users, ai
from backend.di import init_di_web
from backend.core.log_settings import setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI) -> AbstractAsyncContextManager[None]:
    yield
    await app.state.dishka_container.close()


def create_app() -> FastAPI:
    app = FastAPI(
        title="Telegram AI Assistant Backend",
        description="Backend for handling AI requests from Telegram bot.",
        lifespan=lifespan,
    )
    app.include_router(ai.router)
    app.include_router(users.router)
    setup_logging()
    init_di_web(app)
    return app


if __name__ == "__main__":
    uvicorn.run("backend.main:create_app", port=8080, factory=True, reload=True)
