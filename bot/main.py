import asyncio
import httpx
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import CommandStart

from backend.core.config import settings

# Инициализация бота и диспетчера
bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

# Хэндлер на команду /start
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    async with httpx.AsyncClient() as client:
        try:
            # Проверяем, существует ли пользователь в базе данных
            response = await client.get(f"{settings.BACKEND_URL}/api/v1/users/by_telegram_id/{message.from_user.id}")
            if response.status_code == 404:
                # Если пользователя нет, регистрируем его
                user_data = {
                    "telegram_id": message.from_user.id,
                    "username": message.from_user.username if message.from_user.username else f"user_{message.from_user.id}",
                    "full_name": message.from_user.full_name
                }
                registration_response = await client.post(f"{settings.BACKEND_URL}/api/v1/users/", json=user_data)
                registration_response.raise_for_status()
                await message.reply("Привет! Я твой ИИ ассистент. Я тебя зарегистрировал. Задай мне вопрос.")
            elif response.status_code == 200:
                await message.reply("С возвращением! Я твой ИИ ассистент. Задай мне вопрос.")
            else:
                response.raise_for_status()
        except httpx.RequestError as exc:
            await message.reply(f"Произошла ошибка при запросе к бэкенду: {exc}")
        except httpx.HTTPStatusError as exc:
            await message.reply(f"Бэкенд вернул ошибку {exc.response.status_code}: {exc.response.text}")
        except Exception as e:
            await message.reply(f"Произошла неожиданная ошибка: {e}")

# Хэндлер для всех остальных сообщений
@dp.message()
async def handle_message(message: types.Message):
    if message.text:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{settings.BACKEND_URL}/api/v1/generate_response",
                    json={
                        "message": message.text,
                        "chat_id": message.chat.id
                    }
                )
                response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
                ai_message = response.json()
                await message.reply(ai_message.get("response", "Произошла ошибка при получении ответа от ИИ."))
            except httpx.RequestError as exc:
                await message.reply(f"Произошла ошибка при запросе к бэкенду: {exc}")
            except httpx.HTTPStatusError as exc:
                await message.reply(f"Бэкенд вернул ошибку {exc.response.status_code}: {exc.response.text}")
            except Exception as e:
                await message.reply(f"Произошла неожиданная ошибка: {e}")
    else:
        await message.reply("Я могу обрабатывать только текстовые сообщения.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main()) 