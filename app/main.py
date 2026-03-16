from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import asyncio
from datetime import datetime
import threading
import time

from .config import Config
from .monitor import APIMonitor

# Initialize FastAPI app
app = FastAPI(title="API Product Monitoring Dashboard")

# Setup templates
templates = Jinja2Templates(directory="app/templates")

# Initialize config and monitor
config = Config()
monitor = APIMonitor(config)

# Store monitoring results
monitoring_results = []
last_check_time = None

def run_monitoring():
    """Function to run monitoring in background thread"""
    global monitoring_results, last_check_time
    
    while True:
        try:
            # Run monitoring check
            result = monitor.check_all()
            monitoring_results.append(result)
            last_check_time = datetime.now()
            
            # Keep only last 100 results
            if len(monitoring_results) > 100:
                monitoring_results.pop(0)
            
            # Wait for next check
            time.sleep(config.CHECK_INTERVAL)
            
        except Exception as e:
            print(f"Monitoring error: {e}")
            time.sleep(5)

@app.on_event("startup")
async def startup_event():
    """Start background monitoring when app starts"""
    thread = threading.Thread(target=run_monitoring, daemon=True)
    thread.start()
    print(f"🚀 Monitoring started - checking API at {config.API_URL} every {config.CHECK_INTERVAL} seconds")

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Main dashboard page"""
    current_result = monitoring_results[-1] if monitoring_results else None
    summary = monitor.get_summary()
    
    # Get last 10 results for history
    history = monitoring_results[-10:] if monitoring_results else []
    
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "current": current_result,
            "summary": summary,
            "history": history,
            "api_url": config.API_URL,
            "last_check": last_check_time
        }
    )

@app.get("/api/status")
async def get_status():
    """Get current API status"""
    if monitoring_results:
        return monitoring_results[-1]
    return {"status": "waiting", "message": "No monitoring data yet"}

@app.get("/api/history")
async def get_history(limit: int = 10):
    """Get monitoring history"""
    return monitoring_results[-limit:] if monitoring_results else []

@app.get("/api/summary")
async def get_summary():
    """Get monitoring summary"""
    return monitor.get_summary()

@app.get("/api/check-now")
async def check_now():
    """Force immediate check"""
    result = monitor.check_all()
    monitoring_results.append(result)
    return result

@app.get("/api/logs")
async def get_logs(lines: int = 50):
    """Get recent logs"""
    try:
        with open(config.LOG_FILE, 'r') as f:
            all_logs = f.readlines()
            recent_logs = all_logs[-lines:] if all_logs else []
        return {"logs": recent_logs}
    except Exception as e:
        return {"error": str(e), "logs": []}

@app.get("/health")
async def health():
    """Health check for monitoring service"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "monitoring_api": config.API_URL,
        "checks_performed": len(monitoring_results)
    }

@app.get("/api/endpoints")
async def get_endpoints():
    """Get list of monitored endpoints"""
    return {
        "endpoints": config.ENDPOINTS,
        "total": len(config.ENDPOINTS)
    }