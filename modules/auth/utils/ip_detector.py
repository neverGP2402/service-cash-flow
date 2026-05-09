import requests
import logging
from typing import Optional
from flask import request


class IPDetector:
    """Production-ready client IP detection"""
    
    def __init__(self):
        # Create logger without Flask dependency
        self.logger = logging.getLogger(f'{__name__}.{self.__class__.__name__}')
        
        # Configure logger if not already configured
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s [%(levelname)s] %(name)s - %(message)s'
            )
            handler.setFormatter(formatter)
            handler.setLevel(logging.INFO)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)
    
    def detect_client_ip(self) -> str:
        """Detect client IP using reliable methods"""
        
        # Method 1: Try HTTP headers first (most reliable for production)
        ip = self._get_from_headers()
        if ip and self._validate_ip(ip):
            self.logger.info(f"IP detected from headers: {ip}")
            return ip
        
        # Method 2: Use Flask's remote_addr (direct connection)
        if hasattr(request, 'remote_addr') and request.remote_addr:
            if self._validate_ip(request.remote_addr):
                self.logger.info(f"IP detected from remote_addr: {request.remote_addr}")
                return request.remote_addr
        
        # Method 3: Try simple external service (fallback)
        ip = self._get_simple_external_ip()
        if ip and self._validate_ip(ip):
            self.logger.info(f"IP detected from external service: {ip}")
            return ip
        
        # Final fallback - use localhost for development
        self.logger.warning("Could not detect client IP, using localhost")
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
        
        for header in headers_to_check:
            try:
                if request.headers.get(header):
                    ip = request.headers.get(header)
                    
                    # Handle comma-separated IPs (X-Forwarded-For can have multiple)
                    if ',' in ip:
                        ip = ip.split(',')[0].strip()
                    
                    if self._validate_ip(ip):
                        return ip
            except Exception as e:
                self.logger.debug(f"Header {header} check failed: {e}")
                continue
        
        return None
    
    def _get_simple_external_ip(self) -> Optional[str]:
        """Get IP from simple external service"""
        try:
            # Use ipify - most reliable
            response = requests.get('https://api.ipify.org?format=json', timeout=5)
            if response.status_code == 200:
                data = response.json()
                ip = data.get('ip')
                if ip and self._validate_ip(ip):
                    return ip
        except Exception as e:
            self.logger.debug(f"ipify service failed: {e}")
        
        try:
            # Fallback to ipapi
            response = requests.get('https://ipapi.co/json/', timeout=5)
            if response.status_code == 200:
                data = response.json()
                ip = data.get('ip')
                if ip and self._validate_ip(ip):
                    return ip
        except Exception as e:
            self.logger.debug(f"ipapi service failed: {e}")
        
        return None
    
    def _validate_ip(self, ip: str) -> bool:
        """Validate IP address format"""
        try:
            import ipaddress
            ipaddress.ip_address(ip)
            return True
        except ValueError:
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
            'privacy_note': 'Server detects client IP automatically'
        }


# Singleton instance - production ready
ip_detector = IPDetector()
