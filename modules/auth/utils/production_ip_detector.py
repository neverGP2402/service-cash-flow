import requests
import logging
from typing import Optional
from flask import request


class ProductionIPDetector:
    """Production-ready IP detector with proper logging"""
    
    def __init__(self):
        # Create production logger
        self.logger = logging.getLogger('production.ip_detector')
        
        # Configure logger if not already configured
        if not self.logger.handlers:
            # Console handler for development
            console_handler = logging.StreamHandler()
            console_formatter = logging.Formatter(
                '%(asctime)s [%(levelname)s] %(name)s - %(message)s'
            )
            console_handler.setFormatter(console_formatter)
            console_handler.setLevel(logging.INFO)
            self.logger.addHandler(console_handler)
            
            # File handler for production (if logs directory exists)
            try:
                import os
                log_dir = os.path.join(os.path.dirname(__file__), '../../../logs')
                if os.path.exists(log_dir):
                    file_handler = logging.FileHandler(
                        os.path.join(log_dir, 'ip_detection.log')
                    )
                    file_handler.setFormatter(console_formatter)
                    file_handler.setLevel(logging.INFO)
                    self.logger.addHandler(file_handler)
            except Exception:
                pass  # Skip file handler if directory doesn't exist
            
            self.logger.setLevel(logging.INFO)
    
    def detect_client_ip(self) -> str:
        """Detect client IP using production-ready methods"""
        
        self.logger.info("Starting IP detection...")
        
        # Method 1: Try HTTP headers first
        ip = self._get_from_headers()
        if ip and self._validate_ip(ip):
            self.logger.info(f"IP detected from headers: {ip}")
            return ip
        
        self.logger.info("No IP from headers, trying remote_addr...")
        
        # Method 2: Use Flask's remote_addr
        try:
            if hasattr(request, 'remote_addr') and request.remote_addr:
                if self._validate_ip(request.remote_addr):
                    self.logger.info(f"IP detected from remote_addr: {request.remote_addr}")
                    return request.remote_addr
        except Exception as e:
            self.logger.error(f"Remote_addr detection failed: {e}")
        
        self.logger.info("No IP from remote_addr, trying external service...")
        
        # Method 3: Try external service
        ip = self._get_simple_external_ip()
        if ip and self._validate_ip(ip):
            self.logger.info(f"IP detected from external service: {ip}")
            return ip
        
        self.logger.warning("Could not detect client IP, using localhost fallback")
        return '127.0.0.1'
    
    def _get_from_headers(self) -> Optional[str]:
        """Get IP from HTTP headers"""
        headers_to_check = [
            'X-Forwarded-For',
            'X-Real-IP', 
            'X-Client-IP',
            'CF-Connecting-IP',
            'True-Client-IP',
            'X-Cluster-Client-IP',
            'X-Original-Forwarded-For'
        ]
        self.logger.info(f"request.headers: {request.headers}")
        
        for header in headers_to_check:
            try:
                value = request.headers.get(header)
                self.logger.debug(f"Header {header}: {value}")
                
                if value:
                    ip = value
                    
                    # Handle comma-separated IPs
                    if ',' in ip:
                        ip = ip.split(',')[0].strip()
                        self.logger.debug(f"Comma-separated IP, using first: {ip}")
                    
                    if self._validate_ip(ip):
                        self.logger.info(f"Valid IP found in header {header}: {ip}")
                        return ip
            except Exception as e:
                self.logger.error(f"Header {header} error: {e}")
                continue
        
        self.logger.debug("No valid IP found in headers")
        return None
    
    def _get_simple_external_ip(self) -> Optional[str]:
        """Get IP from external service"""
        try:
            self.logger.info("Trying ipify service...")
            response = requests.get('https://api.ipify.org?format=json', timeout=5)
            if response.status_code == 200:
                data = response.json()
                ip = data.get('ip')
                self.logger.debug(f"ipify response: {data}")
                if ip and self._validate_ip(ip):
                    return ip
        except Exception as e:
            self.logger.error(f"ipify error: {e}")
        
        try:
            self.logger.info("Trying ipapi service...")
            response = requests.get('https://ipapi.co/json/', timeout=5)
            if response.status_code == 200:
                data = response.json()
                ip = data.get('ip')
                self.logger.debug(f"ipapi response: {data}")
                if ip and self._validate_ip(ip):
                    return ip
        except Exception as e:
            self.logger.error(f"ipapi error: {e}")
        
        self.logger.info("External services failed")
        return None
    
    def _validate_ip(self, ip: str) -> bool:
        """Validate IP address format"""
        try:
            import ipaddress
            ipaddress.ip_address(ip)
            self.logger.debug(f"IP {ip} is valid")
            return True
        except ValueError:
            self.logger.error(f"IP {ip} is invalid")
            return False
    
    def get_detection_info(self) -> dict:
        """Get information about IP detection process"""
        return {
            'methods_available': [
                'HTTP Headers',
                'Flask remote_addr',
                'External Services'
            ],
            'current_method': 'Production Auto-detection',
            'reliability': 'High',
            'privacy_note': 'Server detects client IP automatically',
            'logging': 'Console + File (if available)'
        }


# Singleton instance - production ready
production_ip_detector = ProductionIPDetector()
