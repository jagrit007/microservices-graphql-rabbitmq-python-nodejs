from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/recommendations")

class MongoDBConnection:
    client: AsyncIOMotorClient = None

    def connect(self):
        if self.client is None:
            self.client = AsyncIOMotorClient(MONGO_URI)
            print("Connected to MongoDB")

    def get_database(self):
        return self.client.get_database()

    def close(self):
        if self.client:
            self.client.close()
            print("Disconnected from MongoDB")

# Singleton instance
mongodb = MongoDBConnection()

async def get_db():
    mongodb.connect()
    return mongodb.get_database()
