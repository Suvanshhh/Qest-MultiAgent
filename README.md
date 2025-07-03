# Multi-Agent Support & Analytics Platform

A full-stack project featuring two intelligent backend agents (Support Agent and Dashboard Agent) powered by [CrewAI](https://github.com/joaomdmoura/crewAI), FastAPI, and MongoDB, with a modern React frontend.  
**All components are fully dockerized for easy deployment.**

## 🚀 Features

- **Support Agent**:  
  - Handles service-related queries (class/course info, order/payment status, client search, etc.)
  - Can create orders and client enquiries via an external API interface.
- **Dashboard Agent**:  
  - Provides business analytics (revenue, outstanding payments, client insights, trends, etc.)
  - Aggregates and reports on data from MongoDB.

- **Modern React Frontend**:  
  - Clean UI for natural language queries to both agents.
  - Beautiful, user-friendly display of results.

- **MongoDB Integration**:  
  - All agent logic is powered by real data in MongoDB collections.

- **Dockerized**:  
  - One command to run everything (backend, frontend, MongoDB).

## 🗂️ Project Structure

```
QEST/
├── multiagent-backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── agents/
│   ├── tools/
│   ├── api/
│   ├── schemas/
│   └── utils.py
├── multiagent-frontend/
│   ├── package.json
│   ├── Dockerfile
│   ├── public/
│   └── src/
└── docker-compose.yml
```

## ⚡ Quick Start (Docker)

1. **Clone this repository**

    ```bash
    git clone 
    cd QEST
    ```

2. **Build and run all services**

    ```bash
    docker-compose up --build
    ```

3. **Access the app**

    - **Frontend:** [http://localhost:3000](http://localhost:3000)
    - **Backend (FastAPI docs):** [http://localhost:8000/docs](http://localhost:8000/docs)
    - **MongoDB:** localhost:27017 (for Compass or CLI)

## 🧩 Functionality Overview

### Support Agent

Handles:
- Client search by name/email/phone
- Viewing enrolled services/status
- Order management (by ID/client, paid/pending)
- Payment info (details, pending dues)
- Class/course discovery (upcoming, by instructor/status)
- Creating client enquiries & orders (via external API)

Sample queries:
- `"What classes are available this week?"`
- `"Has order #12345 been paid?"`
- `"Create an order for Yoga Beginner for client Priya Sharma"`

### Dashboard Agent

Handles:
- Revenue metrics (total, outstanding)
- Client insights (active/inactive, birthdays, new clients)
- Service analytics (enrollment trends, top services, completion rates)
- Attendance reports (percentages, drop-off rates)

Sample queries:
- `"How much revenue did we generate this month?"`
- `"Which course has the highest enrollment?"`
- `"What is the attendance percentage for Pilates?"`

## 🛠️ Local Development (Without Docker)

### Backend

```bash
cd multiagent-backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend

```bash
cd multiagent-frontend
npm install
npm start
```

- Make sure MongoDB is running locally (`mongodb://localhost:27017`).

## 🗄️ MongoDB Collections

- `clients`
- `orders`
- `payments`
- `courses`
- `classes`
- `attendance`

> **Tip:** Use [MongoDB Compass](https://www.mongodb.com/products/compass) to add/view data.

## 🧪 Testing the Agents

- Use the React frontend or Swagger UI (`/docs`) to send natural language queries.
- See the README section “Functionality Overview” for example queries.

## 📝 Customization

- Add more sample data to MongoDB for richer responses.
- Extend the frontend for more advanced visualizations.
- Add authentication or user management as needed.

## 📦 Environment Variables

- The backend reads `MONGO_URI` from environment (set in `docker-compose.yml`).
