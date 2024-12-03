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
    from tg.handlers import start, magazine

    bot = Bot(token="7531001764:AAECqkt7KosOFWh5Lm1zq6Jj6P9eP7-CFZQ")
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_routers(start.router, magazine.router)
    await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())