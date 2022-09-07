import logging
import os

from aiogram import Bot, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import set_webhook, DEFAULT_ROUTE_NAME

# from aiogram.utils.executor import start_webhook

API_TOKEN = os.getenv("API_TOKEN")

# webhook settings
WEBHOOK_HOST = f'https://{os.getenv("DOMAIN")}'
WEBHOOK_PATH = f'/bot/{API_TOKEN}'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# webserver settings
WEBAPP_HOST = os.getenv("WEBAPP_HOST")  # or ip
WEBAPP_PORT = os.getenv("WEBAPP_PORT")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN, parse_mode="HTML")
dispatcher = Dispatcher(bot)
dispatcher.middleware.setup(LoggingMiddleware())


def start_webhook(dp,
                  webhook_path,
                  web_app,
                  *,
                  loop=None,
                  skip_updates=None,
                  on_startup=None,
                  on_shutdown=None,
                  check_ip=False,
                  retry_after=None,
                  route_name=DEFAULT_ROUTE_NAME,
                  **kwargs):
    executor = set_webhook(
        dispatcher=dp,
        webhook_path=webhook_path,
        loop=loop,
        skip_updates=skip_updates,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        check_ip=check_ip,
        retry_after=retry_after,
        route_name=route_name,
        web_app=web_app
    )
    executor.run_app(**kwargs)


################################
@dispatcher.message_handler()
async def echo(message: types.Message):
    # Regular request
    await message.answer(message.text)

    # or reply INTO webhook
    # return SendMessage(message.chat.id, message.text)


async def on_startup_func(_):
    await bot.set_webhook(WEBHOOK_URL)
    # insert code here to run it after start


async def on_shutdown_func(dp):
    logging.warning('Shutting down..')

    # insert code here to run it before shutdown

    # Remove webhook (not acceptable in some cases)
    await bot.delete_webhook()

    # Close DB connection (if used)
    await dp.storage.close()
    await dp.storage.wait_closed()

    logging.warning('Bye!')


if __name__ == '__main__':
    from server import app

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
