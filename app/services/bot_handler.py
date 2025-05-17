from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from app.config import API_KEY, logger
from app.services.wallet_lookup import get_wallet_by_telegram_id
from app.services.solana_client import get_sol_balance
from app.services.ai_signals import generate_signal
import httpx
import pandas as pd
import os

from sqlalchemy.orm import Session
from database.db import SessionLocal
from database.models import UserWallet

# In-memory user registry (later replace with DB)
linked_wallets = {}

# FASTAPI URL
FASTAPI_URL = "https://aego.up.railway.app"  # Your deployed API

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    message = f"👋 Hello {user.first_name}, welcome to AegoBot.\n" \
              "Use /linkwallet <your_wallet_address> to get started."
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)

# /linkwallet command
async def link_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if len(context.args) != 1:
        await update.message.reply_text("❗ Usage: /linkwallet <your_wallet_address>")
        return

    wallet = context.args[0]  # ✅ Define it here!
    save_wallet(str(user_id), wallet)  # Now it's defined
    logger.info(f"User {user_id} linked wallet: {wallet}")

    await update.message.reply_text(f"✅ Wallet {wallet} linked to your Telegram account!")


def save_wallet(telegram_id: str, wallet: str):
    db: Session = SessionLocal()
    existing = db.query(UserWallet).filter_by(telegram_id=telegram_id).first()

    if existing:
        existing.wallet_address = wallet
    else:
        new = UserWallet(telegram_id=telegram_id, wallet_address=wallet)
        db.add(new)

    db.commit()
    db.close()


# /status command
async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = str(update.effective_user.id)
    wallet = get_wallet_by_telegram_id(telegram_id)

    if wallet:
        await update.message.reply_text(f"🔗 Your linked wallet:\n`{wallet}`", parse_mode="Markdown")
    else:
        await update.message.reply_text("❌ You haven't linked a wallet yet.\nUse `/linkwallet <your_wallet_address>`.")


# /balance command
async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = str(update.effective_user.id)

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{FASTAPI_URL}/api/balance/{telegram_id}")
        data = response.json()

        if "error" in data:
            await update.message.reply_text(f"❌ {data['error']}")
        else:
            await update.message.reply_text(
                f"💰 Your balance: {data['balance']:.4f} SOL\n📍Wallet: `{data['wallet']}`",
                parse_mode="Markdown"
            )


# ✅ New /signal command
async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = str(update.effective_user.id)
    wallet = get_wallet_by_telegram_id(telegram_id)

    if not wallet:
        await update.message.reply_text("❌ You haven't linked a wallet.\nUse /linkwallet <wallet_address> first.")
        return

    # 🚀 For now, we are using sample features
    # Next step will be live market data
    features = pd.DataFrame({
        'open': [20.5],
        'high': [21.0],
        'low': [20.2],
        'close': [20.8],
        'volume': [15000]
    })

    # Call the AI signal generator
    signal_type, confidence = generate_signal(features)

    if signal_type == "⚠️ Error":
        await update.message.reply_text("❌ There was an error generating the signal. Try again later.")
        return

    # Response Message
    message = (
        f"🔔 *Market Signal for your wallet:*\n\n"
        f"{signal_type}\n"
        f"🤖 *Confidence:* {confidence}%\n"
        f"📍 *Wallet:* `{wallet}`"
    )

    await update.message.reply_text(message, parse_mode="Markdown")


# Register command handlers
bot_app = ApplicationBuilder().token(API_KEY).build()
bot_app.add_handler(CommandHandler("start", start))
bot_app.add_handler(CommandHandler("linkwallet", link_wallet))
bot_app.add_handler(CommandHandler("status", status))
bot_app.add_handler(CommandHandler("balance", balance))
bot_app.add_handler(CommandHandler("signal", signal))
