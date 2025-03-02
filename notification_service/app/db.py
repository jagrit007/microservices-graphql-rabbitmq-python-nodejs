from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from fastapi import Depends
import logging
import os


# Environment Variables
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DATABASE = os.getenv("MONGO_DATABASE", "notification_service")

class MongoDBConnectionManager:
    """
    MongoDB Connection Manager for singleton pattern.
    Ensures a single MongoDB client instance is used.
    """
    client: AsyncIOMotorClient = None

    def connect(self):
        """
        Initialize MongoDB client if not already connected.
        """
        if self.client is None:
            self.client = AsyncIOMotorClient(MONGO_URI)
            logging.info("Connected to MongoDB.")

    def close(self):
        """
        Close MongoDB client connection.
        """
        if self.client:
            self.client.close()
            logging.info("Disconnected from MongoDB.")

    def get_database(self) -> AsyncIOMotorDatabase:
        """
        Returns the MongoDB database instance.
        """
        return self.client[MONGO_DATABASE]

# Singleton instance
mongodb_connection = MongoDBConnectionManager()

async def get_db() -> AsyncIOMotorDatabase:
    """
    Dependency for getting MongoDB database instance.
    """
    mongodb_connection.connect()
    return mongodb_connection.get_database()
