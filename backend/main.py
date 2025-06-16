from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from backend.api.v1.endpoints import users, ai

app = FastAPI(
    title="Telegram AI Assistant Backend",
    description="Backend for handling AI requests from Telegram bot."
)

app.include_router(ai.router, prefix="/api/v1", tags=["AI"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])

@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "Backend is running!"}

# В будущем здесь будут подключаться другие маршруты из backend/app/api/ 