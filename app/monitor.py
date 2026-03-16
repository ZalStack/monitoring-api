import requests
import time
import logging
from datetime import datetime
from typing import Dict, List, Any
from pathlib import Path
import psutil
import json

class APIMonitor:
    def __init__(self, config):
        self.config = config
        self.failed_attempts = 0
        self.metrics = {
            'total_checks': 0,
            'successful_checks': 0,
            'failed_checks': 0,
            'total_response_time': 0,
            'endpoint_stats': {}
        }
        
        # Setup logging
        self.setup_logging()
        
    def setup_logging(self):
        """Setup logging configuration"""
        # Buat folder data jika belum ada
        log_dir = Path(self.config.LOG_FILE).parent
        log_dir.mkdir(exist_ok=True)
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.config.LOG_FILE),
                logging.StreamHandler()  # Also print to console
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def check_api_health(self) -> Dict[str, Any]:
        """Check API health by calling root endpoint"""
        try:
            start_time = time.time()
            response = requests.get(
                f"{self.config.API_URL}/",
                timeout=5
            )
            response_time = (time.time() - start_time) * 1000  # Convert to ms
            
            status = 'up' if response.status_code == 200 else 'degraded'
            
            result = {
                'status': status,
                'status_code': response.status_code,
                'response_time_ms': round(response_time, 2),
                'timestamp': datetime.now().isoformat(),
                'url': f"{self.config.API_URL}/"
            }
            
            self.logger.info(f"Health check: {status} - {response_time}ms")
            return result
            
        except requests.exceptions.ConnectionError:
            result = {
                'status': 'down',
                'error': 'Connection refused - API is down',
                'timestamp': datetime.now().isoformat(),
                'url': f"{self.config.API_URL}/"
            }
            self.logger.error(f"Health check failed: API is down")
            return result
            
        except requests.exceptions.Timeout:
            result = {
                'status': 'down',
                'error': 'Timeout - API not responding',
                'timestamp': datetime.now().isoformat(),
                'url': f"{self.config.API_URL}/"
            }
            self.logger.error(f"Health check failed: Timeout")
            return result
            
        except Exception as e:
            result = {
                'status': 'down',
                'error': str(e),
                'timestamp': datetime.now().isoformat(),
                'url': f"{self.config.API_URL}/"
            }
            self.logger.error(f"Health check failed: {e}")
            return result
    
    def check_endpoint(self, endpoint: Dict) -> Dict[str, Any]:
        """Check specific endpoint"""
        try:
            url = f"{self.config.API_URL}{endpoint['path']}"
            start_time = time.time()
            
            if endpoint['method'] == 'GET':
                response = requests.get(url, timeout=5)
            elif endpoint['method'] == 'POST':
                # For POST, we'll use a test product
                response = requests.post(
                    url, 
                    json=self.config.SAMPLE_PRODUCT,
                    timeout=5
                )
            else:
                response = requests.get(url, timeout=5)
            
            response_time = (time.time() - start_time) * 1000
            
            # Determine status
            if response.status_code < 400:
                status = 'up'
                self.failed_attempts = 0
            elif response.status_code < 500:
                status = 'degraded'
                self.failed_attempts += 1
            else:
                status = 'down'
                self.failed_attempts += 1
            
            result = {
                'name': endpoint['name'],
                'path': endpoint['path'],
                'method': endpoint['method'],
                'status': status,
                'status_code': response.status_code,
                'response_time_ms': round(response_time, 2),
                'timestamp': datetime.now().isoformat()
            }
            
            # Update endpoint stats
            if endpoint['name'] not in self.metrics['endpoint_stats']:
                self.metrics['endpoint_stats'][endpoint['name']] = {
                    'total': 0,
                    'success': 0,
                    'failed': 0,
                    'total_time': 0
                }
            
            stats = self.metrics['endpoint_stats'][endpoint['name']]
            stats['total'] += 1
            stats['total_time'] += response_time
            
            if status == 'up':
                stats['success'] += 1
            else:
                stats['failed'] += 1
            
            log_msg = f"Endpoint {endpoint['name']}: {status} - {response_time}ms"
            if status == 'up':
                self.logger.info(log_msg)
            else:
                self.logger.warning(log_msg)
                
            return result
            
        except Exception as e:
            self.failed_attempts += 1
            
            result = {
                'name': endpoint['name'],
                'path': endpoint['path'],
                'method': endpoint['method'],
                'status': 'down',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
            
            self.logger.error(f"Endpoint {endpoint['name']} failed: {e}")
            return result
    
    def get_system_metrics(self) -> Dict[str, Any]:
        """Get system metrics"""
        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Memory usage
            memory = psutil.virtual_memory()
            
            # Disk usage
            disk = psutil.disk_usage('/')
            
            metrics = {
                'cpu': {
                    'percent': cpu_percent,
                    'status': 'normal' if cpu_percent < 80 else 'high'
                },
                'memory': {
                    'percent': memory.percent,
                    'used_mb': round(memory.used / (1024 * 1024), 2),
                    'total_mb': round(memory.total / (1024 * 1024), 2),
                    'status': 'normal' if memory.percent < 80 else 'high'
                },
                'disk': {
                    'percent': disk.percent,
                    'used_gb': round(disk.used / (1024 * 1024 * 1024), 2),
                    'total_gb': round(disk.total / (1024 * 1024 * 1024), 2),
                    'status': 'normal' if disk.percent < 90 else 'high'
                },
                'timestamp': datetime.now().isoformat()
            }
            
            return metrics
        except Exception as e:
            self.logger.error(f"Failed to get system metrics: {e}")
            return {}
    
    def check_all(self) -> Dict[str, Any]:
        """Run all checks"""
        # Get health check
        health_result = self.check_api_health()
        
        # Check all endpoints
        endpoint_results = []
        for endpoint in self.config.ENDPOINTS:
            result = self.check_endpoint(endpoint)
            endpoint_results.append(result)
        
        # Get system metrics
        system_metrics = self.get_system_metrics()
        
        # Update global metrics
        self.metrics['total_checks'] += 1
        if health_result['status'] == 'up':
            self.metrics['successful_checks'] += 1
        else:
            self.metrics['failed_checks'] += 1
        
        if 'response_time_ms' in health_result:
            self.metrics['total_response_time'] += health_result['response_time_ms']
        
        # Compile results
        results = {
            'timestamp': datetime.now().isoformat(),
            'health': health_result,
            'endpoints': endpoint_results,
            'system': system_metrics,
            'alert': self.failed_attempts >= self.config.ALERT_THRESHOLD,
            'failed_attempts': self.failed_attempts
        }
        
        # Send alert if needed
        if results['alert']:
            self.send_alert(results)
        
        return results
    
    def send_alert(self, results: Dict):
        """Send alert (simplified - just print and log)"""
        alert_msg = f"⚠️ ALERT: {self.failed_attempts} consecutive failures detected!"
        self.logger.warning(alert_msg)
        print(f"\n{'='*50}")
        print(alert_msg)
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print('='*50)
    
    def get_summary(self) -> Dict:
        """Get monitoring summary"""
        avg_response_time = 0
        if self.metrics['successful_checks'] > 0:
            avg_response_time = self.metrics['total_response_time'] / self.metrics['successful_checks']
        
        uptime = 0
        if self.metrics['total_checks'] > 0:
            uptime = (self.metrics['successful_checks'] / self.metrics['total_checks']) * 100
        
        # Calculate endpoint averages
        endpoint_avg = {}
        for name, stats in self.metrics['endpoint_stats'].items():
            if stats['success'] > 0:
                endpoint_avg[name] = round(stats['total_time'] / stats['success'], 2)
            else:
                endpoint_avg[name] = 0
        
        return {
            'total_checks': self.metrics['total_checks'],
            'successful_checks': self.metrics['successful_checks'],
            'failed_checks': self.metrics['failed_checks'],
            'uptime_percentage': round(uptime, 2),
            'average_response_time_ms': round(avg_response_time, 2),
            'current_failures': self.failed_attempts,
            'endpoint_average_response': endpoint_avg
        }