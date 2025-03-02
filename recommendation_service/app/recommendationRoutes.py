from fastapi import APIRouter, Depends
from .recommendationController import get_recommendation
from .db import get_db
from motor.motor_asyncio import AsyncIOMotorDatabase

recommendation_router = APIRouter()

@recommendation_router.get("/{user_id}")
async def fetch_recommendations(user_id: int, db: AsyncIOMotorDatabase = Depends(get_db)):
    """
    API route to fetch personalized recommendations for a user.
    """
    return await get_recommendation(user_id, db)
