const amqp = require("amqplib");
const { saveNotificationToDB } = require("./controllers/notificationController");

const RABBITMQ_HOST = process.env.RABBITMQ_HOST || "rabbitmq";
const RABBITMQ_USER = process.env.RABBITMQ_USER || "user";
const RABBITMQ_PASS = process.env.RABBITMQ_PASS || "password";
const QUEUE_NAME = process.env.RABBITMQ_QUEUE || "recommendation_queue";

async function connectRabbitMQ() {
  try {
    const connection = await amqp.connect(`amqp://${RABBITMQ_USER}:${RABBITMQ_PASS}@${RABBITMQ_HOST}`);
    const channel = await connection.createChannel();
    await channel.assertQueue(QUEUE_NAME, { durable: true });

    console.log("🐇 Connected to RabbitMQ, waiting for messages...");

    channel.consume(QUEUE_NAME, async (msg) => {
      if (msg !== null) {
        try {
          const content = JSON.parse(msg.content.toString());
          console.log("📩 Received message:", content);

          await saveNotificationToDB(content);

          channel.ack(msg);
        } catch (error) {
          console.error("❌ Error processing message:", error);
          // Do not acknowledge so RabbitMQ can retry later
        }
      }
    });

  } catch (error) {
    console.error("❌ RabbitMQ Connection Error:", error);
    setTimeout(connectRabbitMQ, 5000); // Retry after 5s
  }
}

module.exports = { connectRabbitMQ };
