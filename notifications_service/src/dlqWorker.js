const { Worker, Queue } = require("bullmq");
const Redis = require("ioredis");
const mongoose = require("mongoose");
const Notification = require("./models/Notification");

const redisConnection = new Redis({
  host: process.env.REDIS_HOST || "redis",
  port: 6379,
  maxRetriesPerRequest: null,
  enableReadyCheck: false,
});

const mongoUri = process.env.MONGO_URI;
if (!mongoUri) {
  console.error("❌ MONGO_URI is missing! Set it in .env");
  process.exit(1);
}

// ✅ Connect to MongoDB
mongoose
  .connect(mongoUri)
  .then(() => console.log("📦 DLQ Worker connected to MongoDB"))
  .catch((err) => {
    console.error("❌ MongoDB Connection Error:", err);
    process.exit(1);
  });

const deadLetterQueue = new Queue("dead_letter_queue", { connection: redisConnection });

const dlqWorker = new Worker(
  "dead_letter_queue",
  async (job) => {
    console.log(`♻️ Retrying failed notification for user ${job.data.userId}: ${job.data.message}`);

    try {
      if (!job.data.userId || !job.data.message) {
        throw new Error("❌ Invalid notification data in DLQ - Missing required fields.");
      }

      const notification = new Notification({
        user_id: job.data.userId,
        content: job.data.message,
        type: job.data.type || "general",
      });

      await notification.save();
      console.log(`✅ DLQ Job ${job.id} - Notification saved for user ${job.data.userId}`);

      // ✅ If successful, remove from DLQ
      await deadLetterQueue.remove(job.id);
    } catch (error) {
      console.error(`❌ DLQ Job ${job.id} failed again:`, error);
      throw error; // 🚨 If it fails again, it'll stay in the DLQ
    }
  },
  {
    connection: redisConnection,
    concurrency: 2,           // ✅ Process 2 jobs at a time
    lockDuration: 60000,      // ✅ Lock for 60s to prevent duplicate processing
  }
);

dlqWorker.on("completed", (job) => {
  console.log(`✅ DLQ Job ${job.id} successfully retried!`);
});

dlqWorker.on("failed", (job, err) => {
  console.error(`❌ DLQ Job ${job.id} failed again:`, err);
});

console.log("🚀 DLQ Worker is running...");
