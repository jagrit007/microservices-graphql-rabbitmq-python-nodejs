const Notification = require("../models/Notification");

// 🔹 Standalone function to save notifications to DB (for both Express & RabbitMQ)
const saveNotificationToDB = async (notificationData) => {
  try {
    const { user_id, type, content } = notificationData;

    if (!user_id || !type || !content) {
      throw new Error("Missing required fields");
    }

    // ✅ Check if the same notification already exists
    const existingNotification = await Notification.findOne({
      user_id,
      type,
      content,
    });

    if (existingNotification) {
      console.log("⚠️ Duplicate notification detected. Skipping insertion.");
      return existingNotification; // Avoid storing duplicates
    }

    const notification = new Notification({ user_id, type, content });
    const savedNotification = await notification.save();

    console.log("✅ Notification Stored in DB:", savedNotification);
    return savedNotification;
  } catch (error) {
    console.error("❌ Error saving notification:", error);
    throw error;
  }
};

// 🔹 Express Route to create a notification
const createNotificationRoute = async (req, res) => {
  try {
    const savedNotification = await saveNotificationToDB(req.body);
    res.status(201).json(savedNotification);
  } catch (error) {
    res.status(500).json({ message: "Error creating notification", error });
  }
};

// 🔔 Get Unread Notifications for a User
const getUnreadNotifications = async (req, res) => {
  try {
    const notifications = await Notification.find({
      user_id: req.user.user_id, // Extract user from JWT
      read: false
    });

    console.log(`📬 ${notifications.length} unread notifications for user ${req.user.user_id}`);
    res.status(200).json(notifications);
  } catch (error) {
    console.error("❌ Error fetching unread notifications:", error);
    res.status(500).json({ message: "Error fetching notifications", error });
  }
};

// ✅ Mark Notification as Read
const markNotificationAsRead = async (req, res) => {
  try {
    const updatedNotification = await Notification.findByIdAndUpdate(
      req.params.id,
      { read: true },
      { new: true }
    );

    if (!updatedNotification) {
      return res.status(404).json({ message: "Notification not found" });
    }

    console.log(`✅ Notification ${req.params.id} marked as read.`);
    res.status(204).end();
  } catch (error) {
    console.error("❌ Error marking notification as read:", error);
    res.status(500).json({ message: "Error updating notification", error });
  }
};

module.exports = {
  saveNotificationToDB,
  createNotificationRoute,
  getUnreadNotifications,
  markNotificationAsRead
};
