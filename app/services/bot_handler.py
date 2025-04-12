# app/services/bot_handler.py
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from app.config import API_KEY, logger

from sqlalchemy.orm import Session
from database.db import SessionLocal
from database.models import UserWallet

# In-memory user registry (later replace with DB)
linked_wallets = {}

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


# Create bot application
bot_app = ApplicationBuilder().token(API_KEY).build()

# Register command handlers
bot_app.add_handler(CommandHandler("start", start))
bot_app.add_handler(CommandHandler("linkwallet", link_wallet))


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
