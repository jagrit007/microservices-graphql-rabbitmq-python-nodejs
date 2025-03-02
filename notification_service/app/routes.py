from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from .models import Notification
from .crud import create_notification_in_db, get_unread_notifications, mark_notification_as_read
from .db import get_db, mongodb_connection
from .auth import get_current_user

notification_router = APIRouter()

@notification_router.post("/", response_model=Notification)
async def create_notification(notification: Notification, db = Depends(get_db)):
    return await create_notification_in_db(db, notification)


@notification_router.get("/unread/{user_id}")
async def get_unread_notifications_route(
        user_id: int,
        db=Depends(get_db),
        current_user=Depends(get_current_user)
):
    """
    Endpoint to get all unread notifications for the current user.
    """
    print(current_user["user_id"])
    if current_user["user_id"] != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized.")

    notifications = await get_unread_notifications(db, user_id)
    return notifications

@notification_router.put("/{notification_id}/read")
async def mark_notification_as_read_route(
    notification_id: str,
    db=Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Endpoint to mark a notification as read.
    """
    success = await mark_notification_as_read(db, notification_id=notification_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found.")