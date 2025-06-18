from aiogram.dispatcher.router import Router

from bot.dialogs.start import router as start_router

main_router = Router()

main_router.include_routers(
    start_router
)
