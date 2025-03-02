require('dotenv').config();

const express = require('express');
const app = express();

const connectDB = require('./config/db');
const notificationRouter = require('./routes/notificationRoutes');

const { connectRabbitMQ } = require("./rabbitmq");

const { addNotificationJob } = require("./queue");

const { register, httpRequestCounter } = require("./metrics");



// Middleware
app.use(express.json());

// Connect to MongoDB and RabbitMQ
connectDB().then(connectRabbitMQ);

// API to trigger a notification
app.post("/send-notification", async (req, res) => {
  const { user_id, message } = req.body;
  const type = req.body.type || "general";
  await addNotificationJob(user_id, message, type);
  res.json({ message: "Notification scheduled" });
});

// Routes
app.use('/notifications', notificationRouter);


app.use((req, res, next) => {
  res.on("finish", () => {
    httpRequestCounter.labels(req.method, req.path, res.statusCode).inc();
  });
  next();
});

app.get("/metrics", async (req, res) => {
  res.set("Content-Type", register.contentType);
  res.end(await register.metrics());
});



// Start Server
const PORT = process.env.PORT || 8002;
app.listen(PORT, () => {
  console.log(`Notification Service running on port ${PORT}`);
});
