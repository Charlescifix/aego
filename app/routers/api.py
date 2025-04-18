from fastapi import APIRouter
from app.services.wallet_lookup import get_wallet_by_telegram_id
from app.services.solana_client import get_sol_balance

router = APIRouter()

@router.get("/balance/{telegram_id}")
async def get_balance(telegram_id: str):
    wallet = get_wallet_by_telegram_id(telegram_id)
    if not wallet:
        return {"error": "No wallet linked."}

    try:
        sol = await get_sol_balance(wallet)
        return {"wallet": wallet, "balance": sol}
    except Exception as e:
        return {"error": str(e)}
