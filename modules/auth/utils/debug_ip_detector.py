import requests
from typing import Optional
from flask import request


class DebugIPDetector:
    """Debug IP detector with print statements"""
    
    def detect_client_ip(self) -> str:
        """Detect client IP using simple methods with debug prints"""
        
        print("🔍 DEBUG: Starting IP detection...")
        
        # Method 1: Try HTTP headers first
        ip = self._get_from_headers()
        if ip and self._validate_ip(ip):
            print(f"✅ DEBUG: IP detected from headers: {ip}")
            return ip
        
        print("🔍 DEBUG: No IP from headers, trying remote_addr...")
        
        # Method 2: Use Flask's remote_addr
        try:
            if hasattr(request, 'remote_addr') and request.remote_addr:
                if self._validate_ip(request.remote_addr):
                    print(f"✅ DEBUG: IP detected from remote_addr: {request.remote_addr}")
                    return request.remote_addr
        except Exception as e:
            print(f"❌ DEBUG: Remote_addr error: {e}")
        
        print("🔍 DEBUG: No IP from remote_addr, trying external service...")
        
        # Method 3: Try external service
        ip = self._get_simple_external_ip()
        if ip and self._validate_ip(ip):
            print(f"✅ DEBUG: IP detected from external service: {ip}")
            return ip
        
        print("⚠️ DEBUG: No IP detected, using localhost fallback")
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
        
        print(f"🔍 DEBUG: Checking {len(headers_to_check)} headers...")
        
        for header in headers_to_check:
            try:
                value = request.headers.get(header)
                print(f"🔍 DEBUG: Header {header}: {value}")
                
                if value:
                    ip = value
                    
                    # Handle comma-separated IPs
                    if ',' in ip:
                        ip = ip.split(',')[0].strip()
                        print(f"🔍 DEBUG: Comma-separated IP, using first: {ip}")
                    
                    if self._validate_ip(ip):
                        print(f"✅ DEBUG: Valid IP found in header {header}: {ip}")
                        return ip
            except Exception as e:
                print(f"❌ DEBUG: Header {header} error: {e}")
                continue
        
        print("🔍 DEBUG: No valid IP found in headers")
        return None
    
    def _get_simple_external_ip(self) -> Optional[str]:
        """Get IP from external service"""
        try:
            print("🔍 DEBUG: Trying ipify service...")
            response = requests.get('https://api.ipify.org?format=json', timeout=5)
            if response.status_code == 200:
                data = response.json()
                ip = data.get('ip')
                print(f"🔍 DEBUG: ipify response: {data}")
                if ip and self._validate_ip(ip):
                    return ip
        except Exception as e:
            print(f"❌ DEBUG: ipify error: {e}")
        
        try:
            print("🔍 DEBUG: Trying ipapi service...")
            response = requests.get('https://ipapi.co/json/', timeout=5)
            if response.status_code == 200:
                data = response.json()
                ip = data.get('ip')
                print(f"🔍 DEBUG: ipapi response: {data}")
                if ip and self._validate_ip(ip):
                    return ip
        except Exception as e:
            print(f"❌ DEBUG: ipapi error: {e}")
        
        print("🔍 DEBUG: External services failed")
        return None
    
    def _validate_ip(self, ip: str) -> bool:
        """Validate IP address format"""
        try:
            import ipaddress
            ipaddress.ip_address(ip)
            print(f"✅ DEBUG: IP {ip} is valid")
            return True
        except ValueError:
            print(f"❌ DEBUG: IP {ip} is invalid")
            return False


# Singleton instance
debug_ip_detector = DebugIPDetector()
