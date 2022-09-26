from aiogram.utils.exceptions import ChatNotFound, BotBlocked
from aiohttp import web

from telegram.responses import ErrorResponse, OKResponse
from ..aiogram_app import aiogram_routes


@aiogram_routes.get("/send/{user}/{message}")
@aiogram_routes.get("/send/{user}")
@aiogram_routes.post("/send/{user}")
@aiogram_routes.post("/send")
async def send_message(request):
    user = request.match_info.get("user", None) or request.query.get("user", None)
    message = request.match_info.get("message", None) or request.query.get("message", None)

    match user, message:
        case None, None:
            return web.json_response(ErrorResponse(
                error_message="user and message expected"
            ))
        case None, _:
            return web.json_response(ErrorResponse(
                error_message="user expected"
            ))
        case _, None:
            return web.json_response(ErrorResponse(
                error_message="message expected"
            ))
    try:
        from telegram.bot import bot
        message = await bot.send_message(
            chat_id=user,
            text=message
        )
    except ChatNotFound:
        return web.json_response(ErrorResponse(
            error_message=f"user id {user} is not valid"
        ))
    except BotBlocked:
        return web.json_response(ErrorResponse(
            error_message=f"user {user} has been blocked this bot"
        ))

    return web.json_response(OKResponse(
        user=user,
        message=message.text
    ))
