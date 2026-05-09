import requests
from typing import Optional
from flask import request, current_app

class SimpleIPDetector:
    """Simple and reliable client IP detection"""
    
    def detect_client_ip(self) -> str:
        """Detect client IP using simple methods"""
        
        # Get logger inside method to avoid context issues
        logger = current_app.logger
        
        # Method 1: Try HTTP headers first (most reliable for production)
        try:
            ip = self._get_from_headers()
            if ip and self._validate_ip(ip):
                logger.info(f"IP detected from headers: {ip}")
                return ip
        except Exception as e:
            logger.debug(f"Header detection failed: {e}")
        
        # Method 2: Use Flask's remote_addr (direct connection)
        try:
            if hasattr(request, 'remote_addr') and request.remote_addr:
                if self._validate_ip(request.remote_addr):
                    logger.info(f"IP detected from remote_addr: {request.remote_addr}")
                    return request.remote_addr
        except Exception as e:
            logger.debug(f"Remote_addr detection failed: {e}")
        
        # Method 3: Try simple external service (fallback)
        try:
            ip = self._get_simple_external_ip()
            if ip and self._validate_ip(ip):
                logger.info(f"IP detected from external service: {ip}")
                return ip
        except Exception as e:
            logger.warning(f"External IP detection failed: {e}")
        
        # Final fallback - use localhost for development
        logger.warning("Could not detect client IP, using localhost")
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
        print("Headers:", request.headers)
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
                # Skip logging at module level to avoid context issues
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
            # Skip logging at module level to avoid context issues
            pass
        
        try:
            # Fallback to ipapi
            response = requests.get('https://ipapi.co/json/', timeout=5)
            if response.status_code == 200:
                data = response.json()
                ip = data.get('ip')
                if ip and self._validate_ip(ip):
                    return ip
        except Exception as e:
            # Skip logging at module level to avoid context issues
            pass
        
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
            'current_method': 'Simple Auto-detection',
            'reliability': 'High',
            'privacy_note': 'Server detects client IP automatically'
        }


# Singleton instance
simple_ip_detector = SimpleIPDetector()
