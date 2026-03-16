#!/bin/bash

echo "🚀 Starting API Product Monitoring..."
echo "===================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "📥 Installing requirements..."
pip install -r requirements.txt

# Create data directory if it doesn't exist
mkdir -p data

# Run the application
echo "✅ Starting monitoring server..."
echo "📊 Dashboard akan tersedia di: http://localhost:8000"
echo "===================================="
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000