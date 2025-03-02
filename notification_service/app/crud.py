from .models import Notification
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List
from bson import ObjectId


async def create_notification_in_db(db: AsyncIOMotorDatabase, notification: Notification) -> Notification:
    """
    Inserts a new notification into the MongoDB collection.
    """
    result = await db.notifications.insert_one(notification.model_dump(by_alias=True, exclude={"id"}))
    notification.id = str(result.inserted_id)  # Convert ObjectId to string
    return notification


async def get_unread_notifications(db: AsyncIOMotorDatabase, user_id: int) -> List[Notification]:
    """
    Retrieves all unread notifications for a specific user.
    """
    cursor = db.notifications.find({"user_id": user_id, "read": False})
    notifications = await cursor.to_list(length=100)

    print(notifications)

    # Convert ObjectId to string before returning
    # for notification in notifications:
    #     notification["_id"] = str(notification["_id"])

    return [Notification(**notification) for notification in notifications]


async def mark_notification_as_read(db: AsyncIOMotorDatabase, notification_id: str) -> bool:
    """
    Marks a notification as read by its ObjectId.
    """
    result = await db.notifications.update_one(
        {"_id": ObjectId(notification_id)},
        {"$set": {"read": True}},
    )
    return result.modified_count > 0