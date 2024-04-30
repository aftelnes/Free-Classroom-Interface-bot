import asyncio

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

import config

from callback_handlers.inline_callback import callback_handlers_router


bot = Bot(token=config.base_config.BOT_TOKEN)
dp = Dispatcher()
dp.include_routers(callback_handlers_router)



async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

asyncio.run(main())