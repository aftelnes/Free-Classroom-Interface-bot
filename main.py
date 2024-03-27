import asyncio
import os

from aiogram import Bot, Dispatcher
from dotenv import find_dotenv, load_dotenv

#загружаем_все_переменные_окружения(ищем_все_переменные_окружения)
load_dotenv(find_dotenv())

from callback_handlers.inline_callback import callback_handlers_router


bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()
dp.include_routers( callback_handlers_router)



async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

asyncio.run(main())