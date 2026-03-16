Berikut versi yang **lebih rapi, profesional, dan dalam bahasa Inggris** tanpa mengubah atau menambahkan isi dari teks Anda. Saya hanya merapikan struktur dan menerjemahkannya.

---

# 📊 API Monitoring - DevOps Monitoring Tool

## 📋 Description

A simple monitoring tool to monitor the health of backend APIs using **Python** and **FastAPI** with a visual dashboard.

---

## ✨ Key Features

* **Automatic Health Check** – Periodic API checking
* **Visual Dashboard** – Real-time web interface
* **System Metrics** – Monitor CPU, Memory, Disk
* **Endpoint Monitoring** – Monitor multiple endpoints
* **Alert System** – Warnings for repeated failures
* **History & Logging** – Check history and log files

---

## 🛠️ Technologies

Python 3.8+, FastAPI, Uvicorn, Requests, Psutil, Jinja2, Python-dotenv

---

## 📁 Project Structure

```
monitoring-api/
├── requirements.txt
├── .env
├── run.sh / run.bat
├── app/
│   ├── main.py
│   ├── config.py
│   ├── monitor.py
│   └── templates/dashboard.html
└── data/monitoring.log
```

---

## ⚙️ Prerequisites

* Python 3.8+
* Backend API running on port 3000

---

# 🚀 Installation & Running

## 1. Setup Project

```bash
mkdir monitoring-api && cd monitoring-api
```

---

## 2. Virtual Environment

### Linux / Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configuration (.env)

```env
API_URL=http://localhost:3000 # Replace with your backend API URL
CHECK_INTERVAL=30
LOG_FILE=./data/monitoring.log
ALERT_THRESHOLD=3
```

---

## 5. Run

### Via Script

```bash
# Linux / Mac
chmod +x run.sh && ./run.sh

# Windows
run.bat
```

### Manual

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 6. Access Dashboard

```
http://localhost:8000
```

---

# 📊 Dashboard Components

* **Header** – API status, last check, refresh button
* **Alert Box** – Failure notification
* **Summary Cards** – API Health, System Metrics, Uptime
* **Endpoints Status** – Status of each endpoint
* **History Table** – History of the last 10 checks

---

# 🔌 API Endpoints

| Endpoint                | Method | Function       |
| ----------------------- | ------ | -------------- |
| `/`                     | GET    | Dashboard      |
| `/api/status`           | GET    | Current status |
| `/api/history?limit=10` | GET    | History        |
| `/api/summary`          | GET    | Summary        |
| `/api/check-now`        | GET    | Manual check   |
| `/api/logs`             | GET    | View logs      |
| `/health`               | GET    | Health check   |

---

# ⚙️ Endpoint Configuration

Edit `app/config.py`:

```python
ENDPOINTS = [
    {'name': 'Root', 'path': '/', 'method': 'GET'},
    {'name': 'All', 'path': '/api/', 'method': 'GET'},
]
```

Endpoints must be adjusted to match your API routes.

---

# 🐛 Quick Troubleshooting

## API Not Detected

```bash
curl http://localhost:3000  # Replace with your backend API URL
curl http://localhost:8000/api/logs  # Check logs
```

---

## Port 8000 Used

```bash
# Change port
uvicorn app.main:app --port 8001
```

---

## Module Not Found

```bash
pip install -r requirements.txt
```

---

# 🔧 Customization

* **Change interval**: Edit `CHECK_INTERVAL` in `.env`
* **Change threshold**: Edit `ALERT_THRESHOLD` in `.env`
* **Add endpoint**: Edit `ENDPOINTS` in `config.py`

---

# 🚀 Production Deployment

## PM2

```bash
npm install -g pm2
pm2 start "uvicorn app.main:app --host 0.0.0.0 --port 8000" --name monitoring-api
```

---

## Systemd (Linux)

```bash
# Create service file, enable, start
sudo systemctl enable monitoring-api
sudo systemctl start monitoring-api
```

---

# 📝 Logging

Log file: `data/monitoring.log`

```
2024-01-15 10:30:01 - INFO - Health check: up - 45ms
```

---

**Happy monitoring!** 🎉
A simple monitoring tool to monitor your backend API.
