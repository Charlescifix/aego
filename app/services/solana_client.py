from solana.rpc.async_api import AsyncClient
from solders.pubkey import Pubkey
from app.config import SOL_RPC_URL, logger

async def get_sol_balance(address: str) -> float:
    async with AsyncClient(SOL_RPC_URL) as client:
        logger.info(f"📡 Checking balance for wallet: {address}")
        pubkey = Pubkey.from_string(address)
        response = await client.get_balance(pubkey)
        lamports = response.value
        logger.info(f"🧮 Lamports: {lamports}")
        return lamports / 1_000_000_000
