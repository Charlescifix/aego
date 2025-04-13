# app/services/wallet_lookup.py
from sqlalchemy.orm import Session
from database.db import SessionLocal
from database.models import UserWallet

def get_wallet_by_telegram_id(telegram_id: str) -> str | None:
    db: Session = SessionLocal()
    record = db.query(UserWallet).filter_by(telegram_id=telegram_id).first()
    db.close()

    if record:
        return record.wallet_address
    return None
