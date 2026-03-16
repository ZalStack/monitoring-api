# 📊 Monitoring API - DevOps Monitoring Tool

## 📋 Deskripsi
Tools monitoring sederhana untuk memantau kesehatan API backend menggunakan Python dan FastAPI dengan dashboard visual.

## ✨ Fitur Utama
- **Health Check Otomatis** - Pengecekan API berkala
- **Dashboard Visual** - Tampilan web real-time
- **System Metrics** - Monitoring CPU, Memory, Disk
- **Endpoint Monitoring** - Pantau multiple endpoints
- **Alert System** - Peringatan kegagalan berulang
- **History & Logging** - Riwayat pengecekan dan file log

## 🛠️ Teknologi
Python 3.8+, FastAPI, Uvicorn, Requests, Psutil, Jinja2, Python-dotenv

## 📁 Struktur Project
```
monitoring-api-product/
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

## ⚙️ Prasyarat
- Python 3.8+
- Backend API berjalan di port 3000

## 🚀 Instalasi & Menjalankan

### 1. Setup Project
```bash
mkdir monitoring-api&& cd monitoring-api
```

### 2. Virtual Environment
**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```
**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Konfigurasi (.env)
```env
API_URL=http://localhost:3000 # Ganti URL API Backend anda
CHECK_INTERVAL=30
LOG_FILE=./data/monitoring.log
ALERT_THRESHOLD=3
```

### 5. Jalankan
**Via script:**
```bash
# Linux/Mac
chmod +x run.sh && ./run.sh
# Windows
run.bat
```
**Manual:**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 6. Akses Dashboard
```
http://localhost:8000
```

## 📊 Dashboard Components
- **Header** - Status API, last check, refresh button
- **Alert Box** - Notifikasi kegagalan
- **Summary Cards** - API Health, System Metrics, Uptime
- **Endpoints Status** - Status tiap endpoint
- **History Table** - Riwayat 10 pengecekan terakhir

## 🔌 API Endpoints
| Endpoint | Method | Fungsi |
|----------|--------|--------|
| `/` | GET | Dashboard |
| `/api/status` | GET | Status terkini |
| `/api/history?limit=10` | GET | History |
| `/api/summary` | GET | Ringkasan |
| `/api/check-now` | GET | Check manual |
| `/api/logs` | GET | Lihat log |
| `/health` | GET | Health check |

## ⚙️ Konfigurasi Endpoint
Edit `app/config.py`:
```python
ENDPOINTS = [
    {'name': 'Root', 'path': '/', 'method': 'GET'},
    {'name': 'All', 'path': '/api/', 'method': 'GET'},
]
```

Emdpoint di sesuaikan sama route api anda !

## 🐛 Troubleshooting Cepat

**API tidak terbaca:**
```bash
curl http://localhost:3000  # Ganti Url API Backend anda
curl http://localhost:8000/api/logs  # Cek log
```

**Port 8000 used:**
```bash
# Ganti port
uvicorn app.main:app --port 8001
```

**Module not found:**
```bash
pip install -r requirements.txt
```

## 🔧 Kustomisasi
- **Ubah interval**: Edit `CHECK_INTERVAL` di `.env`
- **Ubah threshold**: Edit `ALERT_THRESHOLD` di `.env`
- **Tambah endpoint**: Edit `ENDPOINTS` di `config.py`

## 🚀 Deployment Production

### PM2
```bash
npm install -g pm2
pm2 start "uvicorn app.main:app --host 0.0.0.0 --port 8000" --name monitoring-api
```

### Systemd (Linux)
```bash
# Buat file service, enable, start
sudo systemctl enable monitoring-api
sudo systemctl start monitoring-api
```

## 📝 Logging
File log: `data/monitoring.log`
```
2024-01-15 10:30:01 - INFO - Health check: up - 45ms
```

---

**Selamat mencoba!** 🎉 Tools monitoring sederhana untuk memantau API backend Anda.
