import logging

from aiogram import Bot, types
from aiogram.utils.exceptions import ChatNotFound
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.webhook import SendMessage
from aiogram.utils.executor import set_webhook, DEFAULT_ROUTE_NAME
from aiohttp import web

# from aiogram.utils.executor import start_webhook

API_TOKEN = '5697130439:AAH6KzSBQi4atnc7i8vaTQ3ACDiHviiqBtY'

# webhook settings
WEBHOOK_HOST = 'https://redslow-services.ru'
WEBHOOK_PATH = f'/bot/{API_TOKEN}'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# webserver settings
WEBAPP_HOST = '0.0.0.0'  # or ip
WEBAPP_PORT = 6220

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN, parse_mode="HTML")
dispatcher = Dispatcher(bot)
dispatcher.middleware.setup(LoggingMiddleware())

################################

routes = web.RouteTableDef()


def setup(dp,
          webhook_path,
          *,
          loop=None,
          skip_updates=None,
          on_startup=None,
          on_shutdown=None,
          check_ip=False,
          retry_after=None,
          route_name=DEFAULT_ROUTE_NAME,
          ):
    set_webhook(
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


def start_webhook(dp,
                  webhook_path,
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


# async def get_async_app(web_app):
#     executor = Executor(dp, skip_updates=True)
#     executor.on_startup(on_startup)
#     executor.on_shutdown(on_shutdown)
#     executor._prepare_webhook(WEBHOOK_PATH, app=web_app)
#     await executor._startup_webhook()
#     return web_app
#


@routes.get("")
async def hello(_):
    return web.Response(text="hi")


@routes.post("/aiogram/send")
async def send_message(request):
    user = request.query.get("user", None)
    message = request.query.get("message", None)
    match user, message:
        case None, None:
            return web.Response(text="user and message expected")
        case None, _:
            return web.Response(text="user expected")
        case _, None:
            return web.Response(text="message expected")
    try:
        await bot.send_message(
            chat_id=user,
            text=message
        )
    except ChatNotFound:
        return web.Response(text=f"user id is not valid")
    return web.Response(text=f"message to user #{user} has been send.")


web_app = web.Application()
web_app.add_routes(routes)


################################
@dispatcher.message_handler()
async def echo(message: types.Message):
    # Regular request
    # await bot.send_message(message.chat.id, message.text)

    # or reply INTO webhook
    return SendMessage(message.chat.id, message.text)


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


# setup(
#     dp=dispatcher,
#     webhook_path=WEBHOOK_PATH,
#     on_startup=on_startup_func,
#     on_shutdown=on_shutdown_func,
#     skip_updates=True,
# )
if __name__ == '__main__':
    start_webhook(
        dp=dispatcher,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup_func,
        on_shutdown=on_shutdown_func,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
