from fastapi import APIRouter, Depends
from .db import get_db
from .rabbitmq import publish_message
from .recommendationEngine import generate_recommendations
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime

recommendation_router = APIRouter()

@recommendation_router.get("/{user_id}")
async def get_recommendation(user_id: int, db: AsyncIOMotorDatabase = Depends(get_db)):
    """
    Fetch personalized recommendations and send them via RabbitMQ.
    """
    recommendations = await db.recommendations.find_one({"user_id": user_id})

    if recommendations:
        recommendations["_id"] = str(recommendations["_id"])
    else:
        recommended_products = await generate_recommendations(user_id)
        new_recommendation = {
            "user_id": user_id,
            "products": recommended_products,
            "created_at": datetime.utcnow()
        }
        result = await db.recommendations.insert_one(new_recommendation)
        new_recommendation["_id"] = str(result.inserted_id)
        recommendations = new_recommendation

    # Publish message to RabbitMQ
    publish_message({
        "user_id": user_id,
        "type": "recommendation",
        "content": {"recommended_products": recommendations["products"]}
    })

    return recommendations
