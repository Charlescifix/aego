from fastapi import APIRouter, Request
from telegram import Update
from app.services.bot_handler import bot_app
from app.config import logger

router = APIRouter()

@router.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, bot_app.bot)

    if not bot_app._initialized:
        await bot_app.initialize()

    await bot_app.process_update(update)
    logger.info("Processed Telegram update: %s", data)
    return {"status": "ok"}
