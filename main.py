from aiogram import Bot, Dispatcher
import func_handlers
import asyncio
import logging
import os
from dotenv import load_dotenv, find_dotenv


async def main():
    # логгирование
    logging.basicConfig(level=logging.INFO, filename="logs.log", filemode="w",
                        format="[%(asctime)s] %(levelname)s %(message)s")

    load_dotenv(find_dotenv())
    bot = Bot(token=os.getenv('TOKEN'))
    dp = Dispatcher()

    dp.include_router(func_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
