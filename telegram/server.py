from aiogram.utils.exceptions import ChatNotFound
from aiohttp import web

routes = web.RouteTableDef()


@routes.get("/aiogram/test")
async def aiogram_test(_):
    return web.json_response({
        "status": "ok"
    })


@routes.get("/aiogram/send/{user}/{message}")
@routes.get("/aiogram/send/{user}")
@routes.post("/aiogram/send/{user}")
@routes.post("/aiogram/send")
async def send_message(request):
    user = request.match_info.get("user", None) or request.query.get("user", None)
    message = request.match_info.get("message", None) or request.query.get("message", None)
    match user, message:
        case None, None:
            return web.json_response({
                "status": "error",
                "error": "user and message expected"
            })
        case None, _:
            return web.json_response({
                "status": "error",
                "error": "user expected"
            })
        case _, None:
            return web.json_response({
                "status": "error",
                "error": "message expected"
            })
    try:
        from bot import bot
        message = await bot.send_message(
            chat_id=user,
            text=message
        )
    except ChatNotFound:
        return web.Response(text=f"user id is not valid")
    return web.json_response({
        "status": "ok",
        "user": user,
        "message": message.text
    })


app = web.Application()
app.add_routes(routes)
