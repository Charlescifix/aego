from fastapi import FastAPI
from app.routers import telegram_router, api
from app.config import logger

app = FastAPI(
    title="AegoBot Backend",
    description="AI-powered Telegram trading bot for $AEGO",
    version="1.0.0",
)

# Register Telegram bot webhook router
app.include_router(telegram_router.router, prefix="/telegram", tags=["Telegram Bot"])

# Register other API routes (e.g., dashboard, status, etc.)
app.include_router(api.router, prefix="/api", tags=["API"])

@app.get("/")
async def root():
    logger.info("Root endpoint hit.")
    return {"message": "Welcome to AegoBot API"}
