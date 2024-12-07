import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()

import asyncio
import logging


async def main():
    from aiogram.enums.parse_mode import ParseMode
    from aiogram.fsm.storage.memory import MemoryStorage
    from aiogram import Bot, Dispatcher
    from tg.handlers import start, magazine, pokupka, promocode, refs, admin

    bot = Bot(token="7784007806:AAETx7oWTbo6MbFmCwunf086hK_lCdFlExU")
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_routers(start.router, magazine.router, pokupka.router, promocode.router, refs.router, admin.router)
    await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())