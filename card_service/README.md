# 🚀 FastAPI Card Service – CRUD API with MongoDB & AWS Deployment!

## 📌 Project Overview

This project demonstrates a **FastAPI-based CRUD API** that manages a card database and is fully containerized with **Docker** and deployed to an **AWS EC2 instance**. The database layer uses **MongoDB**, which is also deployed as a container on the same AWS instance.

✅ **Key Features:**

- Create, Read, Update, and Delete cards
- MongoDB as the persistent backend
- Dockerized FastAPI app
- Deployment on AWS EC2 using Docker
- Exposed public API endpoint accessible over the internet
* **Agent Integration:** An OpenAI Agents SDK-based agent is connected to the deployed FastAPI endpoint. The agent can:

  * Add, fetch, update, delete cards using **natural language prompts**
  * Retrieve all cards by a single query

---

## 🛠️ Tech Stack

- **FastAPI** → Backend framework
- **MongoDB** → NoSQL database
- **Docker** → Containerization
- **AWS EC2** → Cloud deployment
- **OpenAgents SDK** → Intelligent agent integration
- **Uvicorn** → ASGI server
- **Pydantic** → Data validation

---

## 🗂️ Project Structure

```
card_service/
├── app/
│   ├── main.py          # FastAPI entry point
│   ├── models.py        # MongoDB models
│   ├── schemas.py       # Pydantic schemas
│   ├── crud.py          # Database operations
│   ├── database.py      # MongoDB connection logic
│   ├── config/
│   │   └── settings.py  # Environment settings
│   └── ...
├── agent/
│   └── agent.py         # OpenAgents SDK agent integration
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── .env
└── README.md
```

---

## 📡 Live Deployment

- **FastAPI Docs:** `http://<AWS_PUBLIC_IP>:8000/docs`
- **MongoDB:** Running on the same EC2 instance (port **27017**)

The API is publicly accessible, and the agent can hit these endpoints directly.

---

## 🤖 Agent Integration

We integrated an **OpenAgents SDK Agent** which:

- Accepts natural language prompts like:

  > "Add a card titled _Meeting Notes_ with description _Important points_. Then list all cards."

- Calls the deployed FastAPI CRUD endpoints
- Performs:

  - Add new cards
  - Fetch cards (by title, ID, or all)
  - Update cards
  - Delete cards

---

## 💡 What I Learned

During this project, I gained hands-on experience with:

✅ **FastAPI** – Designing REST APIs and working with Pydantic schemas.

✅ **MongoDB** – Integration and CRUD operations.

✅ **Dockerization** – Writing Dockerfiles, building images, running containers.

✅ **AWS Deployment** – Launching EC2 instances, exposing ports, deploying containers.

✅ **Networking** – Handling container-to-container and host-to-container communication.

✅ **Agentic AI** – Connecting an intelligent agent to live API endpoints.

✅ **Debugging** – Solving dependency, networking, and permission errors in a cloud environment.

---

## 🐳 How to Run Locally

```bash
# 1. Clone repo
git clone https://github.com/<username>/Fast_API.git
cd Fast_API/card_service

# 2. Build Docker image
docker build -t card_service:latest .

# 3. Run container
docker run -d -p 8000:8000 --env-file .env card_service:latest

# 4. Open docs
http://localhost:8000/docs
```

---

## 🌍 How to Deploy on AWS

1. Launch an **EC2 instance** (Ubuntu)
2. Install Docker & Git
3. Clone repo → `git clone <repo>`
4. Set up `.env` file with your MongoDB URI
5. Build and run container:

   ```bash
   sudo docker build -t card_service:latest .
   sudo docker run -d --network host --env-file .env card_service:latest
   ```

6. Open port **8000** in AWS Security Group
7. Access your API at:

   ```
   http://<EC2_PUBLIC_IP>:8000/docs
   ```


---

## 🎯 Final Notes

This project was a **full-stack DevOps + AI integration experience**:

- Built a FastAPI CRUD service
- Dockerized & deployed it to AWS
- Connected an OpenAgents SDK agent that interacts with the live API

> ✅ Now I have a **cloud-deployed API** + **intelligent agent** fully working together! 🚀

---

**Author:** Muhammad Khurram Shahzad
**GitHub:** [KhurramDevOps](https://github.com/KhurramDevOps)
**Status:** ✔️ Completed & Deployed
