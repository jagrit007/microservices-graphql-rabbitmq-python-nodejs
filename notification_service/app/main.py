import threading
from fastapi import FastAPI
from .routes import notification_router
from .db import mongodb_connection
from .rabbitmq import consume_messages
app = FastAPI(
    title="Notification Service",
    description="API for managing notifications",
    version="1.0.0"
)

def start_rabbitmq_consumer():
    consume_messages()

threading.Thread(target=start_rabbitmq_consumer, daemon=True).start()



# Include Notification Router
app.include_router(notification_router, prefix="/notifications", tags=["Notifications"])

@app.get("/")
async def root():
    return {"message": "Notification Service is healthy!"}

# @app.on_event("startup")
# async def startup_db_client():
#     """
#     Initialize MongoDB connection on app startup.
#     """
#     mongodb_connection.connect()
#
# @app.on_event("shutdown")
# async def shutdown_db_client():
#     """
#     Close MongoDB connection on app shutdown.
#     """
#     mongodb_connection.close()
