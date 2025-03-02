const { Queue } = require("bullmq");
const Redis = require("ioredis");

const redisConnection = new Redis({
  host: process.env.REDIS_HOST || "redis",
  port: 6379,
  maxRetriesPerRequest: null, // ✅ Required for BullMQ
  enableReadyCheck: false,    // ✅ Prevents unnecessary Redis checks
});

const notificationQueue = new Queue("notifications", {
  connection: redisConnection,
  defaultJobOptions: {
    removeOnComplete: true,  // ✅ Auto-remove completed jobs
    removeOnFail: true,      // ✅ Auto-remove failed jobs
    attempts: 3,             // ✅ Retry failed jobs up to 3 times
    backoff: { type: "exponential", delay: 5000 }, // ✅ Wait before retrying
    timeout: 30000,          // ✅ Allow job to process for up to 30s
  },
});

const deadLetterQueue = new Queue("dead_letter_queue", {
  connection: redisConnection,
});

async function addNotificationJob(userId, message, type) {
  await clearOldJobs(notificationQueue); // Clear old repeat jobs
  await notificationQueue.add(
    "sendNotification",
    { userId, message, type },
    { repeat: { cron: "*/5 * * * *" } }
  );
  console.log(`📩 Scheduled notification for user ${userId}`);
}

async function clearOldJobs(queue) {
  const repeatableJobs = await queue.getRepeatableJobs();
  for (let job of repeatableJobs) {
    await queue.removeRepeatableByKey(job.key);
    console.log(`🗑 Removed old job: ${job.key}`);
  }
}


module.exports = { notificationQueue, addNotificationJob, deadLetterQueue };
