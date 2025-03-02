const { Worker, Queue } = require("bullmq");
const Redis = require("ioredis");
const mongoose = require("mongoose");
const Notification = require("./models/Notification");

const redisConnection = new Redis({
  host: process.env.REDIS_HOST || "redis",
  port: 6379,
  maxRetriesPerRequest: null, // ✅ Prevents connection errors
  enableReadyCheck: false,    // ✅ Helps with Redis availability
});

const mongoUri = process.env.MONGO_URI;
if (!mongoUri) {
  console.error("❌ MONGO_URI is missing! Set it in .env");
  process.exit(1);
}

// ✅ Connect to MongoDB
mongoose
  .connect(mongoUri)
  .then(() => console.log("📦 Worker connected to MongoDB"))
  .catch((err) => {
    console.error("❌ MongoDB Connection Error:", err);
    process.exit(1);
  });

const notificationQueue = new Queue("notifications", { connection: redisConnection });
const deadLetterQueue = new Queue("dead_letter_queue", { connection: redisConnection });

const worker = new Worker(
  "notifications",
  async (job) => {
    console.log(`📢 Sending notification to user ${job.data.userId}: ${job.data.message}`);

    try {
      if (!job.data.userId || !job.data.message) {
        throw new Error("❌ Invalid notification data - Missing required fields.");
      }

      const notification = new Notification({
        user_id: job.data.userId,
        content: job.data.message,
        type: job.data.type || "general",
      });

      await notification.save();
      console.log(`✅ Notification saved for user ${job.data.userId}`);
    } catch (error) {
      console.error("❌ Error saving notification:", error);
      throw error; // ✅ Ensures job retries on failure
    }
  },
  {
    connection: redisConnection,
    concurrency: 5,           // ✅ Process up to 5 jobs at a time
    stalledInterval: 30000,   // ✅ Wait 30s before marking as stalled
    lockDuration: 60000,      // ✅ Job lock for 60s to prevent duplicate processing
  }
);

// ✅ Move Failed Jobs to DLQ
worker.on("failed", async (job, err) => {
  console.error(`❌ Job ${job.id} failed:`, err);
  console.log(`🚨 Moving job ${job.id} to DLQ...`);

  await deadLetterQueue.add("failedNotification", job.data);
  console.log(`📦 Job ${job.id} moved to DLQ`);
});

worker.on("completed", (job) => {
  console.log(`✅ Job ${job.id} completed`);
});
