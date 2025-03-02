from fastapi import FastAPI
from .routes import user_router

app = FastAPI(
    title="User Service",
    description="API for managing users",
    version="1.0.0"
)

app.include_router(user_router, prefix="/users", tags=["Users"])
@app.get("/")
def root():
    return {"message": "User Service is healthy!"}