# 🚀 Funding API Backend

This is the backend service for the funding matching platform, built with **FastAPI** and deployed using **Docker** on **Render**.

## 🛠️ Technologies Used

- **FastAPI** 🚀 - High-performance API framework
- **Docker** 🐳 - Containerized deployment
- **Render** ☁️ - Cloud hosting
- **CORS Middleware** 🔒 - Handles frontend requests
- **JSON Data Storage** 📂 - Simulated database

## 🔧 Setup & Run Locally

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/samimagine/bayern.git
cd bayern
```

### 2️⃣ Install Dependencies

Make sure you have Python 3 installed, then run:

```bash
pip install -r requirements.txt
```

### 3️⃣ Run the API Locally

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at **`http://localhost:8000`**.

## 🐳 Docker Deployment

### Build and Run with Docker

```bash
docker build -t bayern .
docker run -p 8000:8000 bayern
```

## 🌍 Deployed on Render

The API is hosted on **Render**, accessible at:  
🔗 **[https://bayern.onrender.com](https://bayern.onrender.com)**

## 🔥 API Endpoints

### 🎯 Find Best Funding Match

**POST** `/find-best-funding`

#### 📥 Request (JSON)

```json
{
  "state": "Bayern",
  "company_size": "Kleinstunternehmen",
  "areas": "Forschung & Innovation",
  "grant": 10000,
  "revenue": 1000
}
```

#### 📤 Response (JSON)

```json
[
  {
    "funding option": "Example Grant",
    "state": "Bayern",
    "grant_volume": 20000,
    "funding_quota": 50,
    "approval_rate": 80,
    "time_required": 3,
    "benefit_cost_score": 7
  }
]
```

If no match is found, it returns a **404** error.

## 🏗️ Future Improvements

- ✅ Implement a real database (PostgreSQL or MongoDB)
- ✅ Add authentication for secure access 🔐
- ✅ Improve error handling and logging
- ✅ Optimize performance for large datasets

🎉 **Contributions & Feedback Welcome!**
