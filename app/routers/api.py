# app/routers/api.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/ping")
async def ping():
    return {"message": "API is alive"}
