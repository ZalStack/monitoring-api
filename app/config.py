import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # API Configuration
    API_URL = os.getenv('API_URL', 'http://localhost:3000')
    CHECK_INTERVAL = int(os.getenv('CHECK_INTERVAL', 30))
    
    # Monitoring Configuration
    LOG_FILE = os.getenv('LOG_FILE', './data/monitoring.log')
    ALERT_THRESHOLD = int(os.getenv('ALERT_THRESHOLD', 3))
    
    # Endpoints untuk dimonitor
    ENDPOINTS = [
        {'name': 'Root', 'path': '/', 'method': 'GET'},
        {'name': 'Get All Products', 'path': '/api/', 'method': 'GET'},
        {'name': 'Get Product by ID', 'path': '/api/', 'method': 'GET'},  # Test with ID 1
    ]
    
    # Sample data untuk testing POST (optional)
    SAMPLE_PRODUCT = {
        'name': 'Test Product',
        'price': 25000,
        'description': 'Product for monitoring test',
        'stock': 5
    }
