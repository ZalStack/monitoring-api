@echo off
echo 🚀 Starting API Product Monitoring...
echo ====================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo 📥 Installing requirements...
pip install -r requirements.txt

REM Create data directory if it doesn't exist
if not exist "data" mkdir data

REM Run the application
echo ✅ Starting monitoring server...
echo 📊 Dashboard akan tersedia di: http://localhost:8000
echo ====================================
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause