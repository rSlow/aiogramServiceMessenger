from aiogram.dispatcher.webhook import DEFAULT_ROUTE_NAME
from aiogram.utils.executor import set_webhook


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
