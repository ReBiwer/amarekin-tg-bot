from aiogram.dispatcher.router import Router

from bot.dialogs.start import router as start_router
from bot.dialogs.user_text import router as user_text

main_router = Router()

main_router.include_routers(
    start_router,
    user_text
)
