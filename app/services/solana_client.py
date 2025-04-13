from solana.rpc.async_api import AsyncClient
from app.config import SOL_RPC_URL
from app.config import logger

async def get_sol_balance(address: str) -> float:
    async with AsyncClient(SOL_RPC_URL) as client:
        logger.info(f"📡 Checking balance for wallet: {address}")
        response = await client.get_balance(address)
        logger.info(f"🧮 Raw response: {response}")
        lamports = response['result']['value']
        return lamports / 1_000_000_000
