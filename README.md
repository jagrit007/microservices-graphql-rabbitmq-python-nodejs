# 📜 Ecommerce Notifications System - Microservices Architecture

## 📌 Overview
This project is a microservices-based architecture that provides user authentication, notifications, and product recommendations, exposed via a GraphQL Gateway for unified API access. It follows an event-driven architecture using RabbitMQ and BullMQ (Redis-based job queues), ensuring scalability, fault tolerance, and async processing.

## 🚀 Key Features
- **Microservices:** User, Notification, Recommendation
- **GraphQL Gateway:** Unified API access
- **Authentication:** JWT-based security
- **Asynchronous Processing:** RabbitMQ & BullMQ (Redis)
- **Dead-Letter Queue (DLQ):** Handles failed jobs
- **Monitoring:** Prometheus & Grafana
- **Dockerized Deployment**

## 📦 Architecture Overview
```
                                +------------------+
                                |  GraphQL Gateway |
                                |  (Apollo Server) |
                                +--------+---------+
                                        |
             +------------+-------------+--------------+
             |             |                 |
      +------v-----+  +----v-----+  +--------v---------+
      | User       |  | Notif.   |  | Recommendation   |
      | Service    |  | Service  |  | Service          |
      +------+-----+  +----+-----+  +--------+---------+
             |         |                 |
     +-------v----+    |          +------v-----+
     |  Postgres  |    |          |  MongoDB   |
     +------------+    |          +------------+
                       |
      +------------------------------------------+
      |                Async Queueing            |
      +------------------------------------------+
               |                        |
       +-------v--------+        +------v-----+
       | BullMQ (Redis) |        |  RabbitMQ  |
       +----------------+        +------------+

```
Each microservice operates independently and communicates asynchronously via RabbitMQ and BullMQ (Redis queues) (or REST API). The GraphQL Gateway provides a unified API to interact with all services.

## 🛠️ Installation & Setup

### 1️⃣ Prerequisites
- Docker & Docker Compose installed
- Ports **4000 (Apollo), 8000-8003, 5672 (RabbitMQ), 6379 (Redis), 3000 (Grafana), 9090 (Prometheus)** open

### 2️⃣ Clone the Repository
```sh
git clone https://github.com/jagrit007/microservices-graphql-rabbitmq-python-nodejs pratilipi
cd pratilipi
```

### 3️⃣ Start Services with Docker Compose
```sh
docker-compose up -d --build
```
👉 This will start all services in the background.

### 4️⃣ Verify Running Containers
```sh
docker ps
```
You should see GraphQL Gateway, User Service, Notification Service, Recommendation Service, RabbitMQ, Redis, and Prometheus running.

### 5️⃣ Access Services
- **GraphQL Gateway:** [http://localhost:4000](http://localhost:4000)
- **Prometheus UI:** [http://localhost:9090](http://localhost:9090)
- **Grafana UI:** [http://localhost:3000](http://localhost:3000)
  - Username: `admin`
  - Password: `admin`
- **RabbitMQ Management UI:** [http://localhost:15672](http://localhost:15672)
  - Username: `guest`
  - Password: `guest`

## ⚡ Services & Endpoints
#### **Postman collection is included in this repository, kindly check the .postman folder and import the collection into your postman!**
---

### 1️⃣ GraphQL Gateway (Port: 4000) [Node.js-Express-Apollo]
- **Base URL:** `http://localhost:4000`
- **GraphQL Endpoint:** `http://localhost:4000/graphql`

🔹 **Example GraphQL Query:**
```graphql
query {
  user(id: 1) {
    id
    email
  }
  notifications(userId: 1) {
    id
    content
    read
  }
  recommendations(userId: 1) {
    userId
    products
  }
}
```

### 2️⃣ User Service (Port: 8050) [Python-FastAPI-Postgresql]
- **Base URL:** `http://localhost:8050`

| Method | Endpoint     | Description                       | Auth Required |
|--------|-------------|-----------------------------------|--------------|
| POST   | `/users`     | Register a new user              | ❌ No        |
| POST   | `/users/login` | Login user & return JWT token  | ❌ No        |
| GET    | `/users/{id}` | Get user details                | ✅ Yes       |
| PUT    | `/users/{id}` | Update user preferences         | ✅ Yes       |

🔹 **Example Login Request:**
```json
{
  "email": "jagrit007@gmail.com",
  "password": "test123"
}
```
**Response:**
```json
{
  "access_token": "jwt_token_here",
  "type": "bearer"
}
```

### 3️⃣ Notification Service (Port: 8002) [Node.js-Express-MongoDB] (also includes python version of this service with MongoDB, kinda broken!)
- **Base URL:** `http://localhost:8002`

| Method | Endpoint                 | Description                      | Auth Required |
|--------|-------------------------|----------------------------------|--------------|
| POST   | `/notifications/`       | Create a new notification       | ❌ No        |
| GET    | `/notifications/unread` | Get unread notifications for a user | ✅ Yes  |
| PUT    | `/notifications/{id}/read` | Mark notification as read      | ✅ Yes       |

🔹 **Example Create Notification Request:**
```json
{
  "user_id": 1,
  "type": "promotions",
  "content": "hello 2",
  "read": false
}
```

### 4️⃣ Recommendation Service (Port: 8003) [Python-FastAPI-MongoDB]
- **Base URL:** `http://localhost:8003`

| Method | Endpoint                  | Description                                | Auth Required |
|--------|--------------------------|--------------------------------------------|--------------|
| GET    | `/recommendations/{id}`  | Get personalized recommendations for a user | ✅ Yes       |

🔹 **Example Recommendation Response:**
```json
{
  "_id": "67c2f236ffad2a706e96182f",
  "user_id": 1,
  "products": ["product_7", "product_9", "product_8"],
  "created_at": "2025-03-01T11:40:38.183000"
}
```

## 📊 Monitoring with Prometheus & Grafana

🔹 **1️⃣ Prometheus Scrape Config (`prometheus.yml`)**
```yaml
global:
  scrape_interval: 5s

scrape_configs:
  - job_name: "redis"
    static_configs:
      - targets: ["redis-exporter:9121"]

  - job_name: "rabbitmq"
    static_configs:
      - targets: ["rabbitmq:15692"]

  - job_name: "notification_service"
    static_configs:
      - targets: ["notification_service:8002"]

  - job_name: "user_service"
    static_configs:
      - targets: ["user_service:8001"]

  - job_name: "recommendation_service"
    static_configs:
      - targets: ["recommendation_service:8003"]

```

🔹 **2️⃣ Metrics Endpoint (Each service exposes `/metrics`)**
- **Notification Service:** [http://localhost:8002/metrics](http://localhost:8002/metrics) (✔)
- **Redis Metrics:** (✔)
- **BullMQ Metrics:** (✔)
- **RabbitMQ Metrics:** (✔)
- **Node.js/Express HTTP Metrics:** (✔)
- **User Service:** (PENDING!)

Kindly check grafana web-ui, I have included dashboards within the project repository.

## 🚑 Troubleshooting

🔹 **Check logs:**
```sh
docker-compose logs -f <service_name>
```
🔹 **Restart a service:**
```sh
docker-compose restart <service_name>
```
🔹 **Stop all services:**
```sh
docker-compose down
```

## ✅ Final Checklist

✔ GraphQL API working? ([http://localhost:4000/graphql](http://localhost:4000/graphql))  
✔ Authentication with JWT? (Bearer `<token>` in headers)  
✔ RabbitMQ & Redis working? (`docker logs notifications_worker`)  
✔ Monitoring available? (Grafana @ [http://localhost:3000](http://localhost:3000))  
✔ DLQ reprocessing jobs? (`docker logs dlq_worker`)  

## 🔐 Security Measures
✔ We can disable opening ports to the host system and rather just expose it to the services in the same docker compose file, or just open port for GraphQL Endpoint. (Only for development purpose I kept all ports open!)
✔ JWT Protected Routes
✔ We can read user_id from the JWT Token instead of explicitly taking it in the url endpoint (I just prefer that for future extensibility)
