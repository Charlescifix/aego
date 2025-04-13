# app/services/solana_client.py
from solana.rpc.async_api import AsyncClient
from app.config import SOL_RPC_URL

async def get_sol_balance(address: str) -> float:
    async with AsyncClient(SOL_RPC_URL) as client:
        response = await client.get_balance(address)
        lamports = response['result']['value']
        return lamports / 1_000_000_000  # Convert from lamports to SOL
