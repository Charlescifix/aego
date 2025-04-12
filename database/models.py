# database/models.py
from sqlalchemy import Column, Integer, String
from database.db import Base

class UserWallet(Base):
    __tablename__ = "user_wallets"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(String, unique=True, index=True)
    wallet_address = Column(String, index=True)
