const axios = require("axios");
const NOTIFICATION_SERVICE_URL = process.env.NOTIFICATION_SERVICE_URL;

async function getNotifications(userId, token) {
  try {
    const response = await axios.get(`${NOTIFICATION_SERVICE_URL}/notifications/unread`, {
      headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
    });

    if (!response.data) return [];

    // Transform response to match GraphQL schema
    const notifications = response.data.map((notification) => ({
      id: notification._id,  // Convert MongoDB _id to id
      userId: notification.user_id,  // Convert snake_case to camelCase
      content: notification.content,
      read: notification.read,
      type: notification.type,
      sentAt: notification.sent_at, // Ensure this field exists in DB
    }));

    return notifications;
  } catch (error) {
    console.error("Error fetching notifications:", error.message);
    return [];
  }
}

module.exports = { getNotifications };
