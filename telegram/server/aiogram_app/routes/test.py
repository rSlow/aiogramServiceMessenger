from aiohttp import web

from telegram.responses import OKResponse
from ..aiogram_app import aiogram_routes


@aiogram_routes.get("/test")
async def aiogram_test(_):
    return web.json_response(OKResponse())
