import logging
import os

from aiogram import Bot, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher

from utils import start_webhook

API_TOKEN = os.getenv("API_TOKEN")

# webhook settings
WEBHOOK_HOST = f'https://{os.getenv("DOMAIN")}:{os.getenv("OUTER_PORT")}'
WEBHOOK_PATH = f'/bot/{API_TOKEN}'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# webserver settings
WEBAPP_HOST = os.getenv("WEBAPP_HOST")  # or ip
WEBAPP_PORT = os.getenv("WEBAPP_PORT")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN, parse_mode="HTML")
dispatcher = Dispatcher(bot)
dispatcher.middleware.setup(LoggingMiddleware())


################################
@dispatcher.message_handler()
async def echo(message: types.Message):
    await message.delete()


async def on_startup_func(_):
    await bot.set_webhook(WEBHOOK_URL)
    # insert code here to run it after start


async def on_shutdown_func(dp):
    logging.warning('Shutting down..')

    await bot.delete_webhook()

    await dp.storage.close()
    await dp.storage.wait_closed()

    logging.warning('Bye!')


if __name__ == '__main__':
    from server.app import app

    start_webhook(
        dp=dispatcher,
        webhook_path=WEBHOOK_PATH,
        web_app=app,
        on_startup=on_startup_func,
        on_shutdown=on_shutdown_func,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
