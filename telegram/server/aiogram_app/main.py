from aiohttp import web

aiogram_routes = web.RouteTableDef()

try:
    from . import routes
except ImportError as ex:
    raise ImportError("Handlers wasn't imported.") from ex

aiogram_app = web.Application()
aiogram_app.add_routes(aiogram_routes)
