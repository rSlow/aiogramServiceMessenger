from aiohttp import web

from aiogram_app.aiogram_app import aiogram_app

app = web.Application()
app.add_subapp(prefix="/aiogram", subapp=aiogram_app)

if __name__ == '__main__':
    web.run_app(app)
