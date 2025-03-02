from fastapi import FastAPI
from .recommendationController import recommendation_router
from .db import mongodb

app = FastAPI(title="Recommendation Service")

@app.on_event("startup")
async def startup_db():
    mongodb.connect()

@app.on_event("shutdown")
async def shutdown_db():
    mongodb.close()

app.include_router(recommendation_router, prefix="/recommendations", tags=["Recommendations"])
