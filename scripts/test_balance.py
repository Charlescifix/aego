# scripts/test_balance.py
import asyncio
from solana.rpc.async_api import AsyncClient

async def main():
    async with AsyncClient("https://api.mainnet-beta.solana.com") as client:
        response = await client.get_balance("YOUR_WALLET_HERE")
        print(response)

asyncio.run(main())
