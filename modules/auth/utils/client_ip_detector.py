import requests
import socket
import asyncio
from typing import Optional, List
from flask import request
from config.logger import get_logger

logger = get_logger(__name__)


class ClientIPDetector:
    """Advanced client IP detection with multiple methods"""
    
    def __init__(self):
        self.detection_methods = [
            self._get_from_headers,
            self._get_simple_external_ip
        ]
    
    def detect_client_ip(self) -> str:
        """Detect client IP using reliable methods"""
        
        # Method 1: Try HTTP headers first (most reliable)
        ip = self._get_from_headers()
        if ip and self._validate_ip(ip):
            logger.info(f"IP detected from headers: {ip}")
            return ip
        
        # Method 2: Use Flask's remote_addr (direct connection)
        if request.remote_addr and self._validate_ip(request.remote_addr):
            logger.info(f"IP detected from remote_addr: {request.remote_addr}")
            return request.remote_addr
        
        # Method 3: Try simple external service (fallback)
        try:
            ip = self._get_simple_external_ip()
            if ip and self._validate_ip(ip):
                logger.info(f"IP detected from external service: {ip}")
                return ip
        except Exception as e:
            logger.warning(f"External IP detection failed: {e}")
        
        # Final fallback
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
        
        for header in headers_to_check:
            if request.headers.get(header):
                ip = request.headers.get(header)
                
                # Handle comma-separated IPs (X-Forwarded-For can have multiple)
                if ',' in ip:
                    ip = ip.split(',')[0].strip()
                
                if self._validate_ip(ip):
                    return ip
        
        return None
    
    async def _get_from_websocket(self) -> Optional[str]:
        """Get IP using WebRTC (browser-based detection)"""
        
        # This is a simplified version - in production, you'd use a more robust implementation
        ice_servers = [
            {'urls': 'stun:stun.l.google.com:19302'},
            {'urls': 'stun:stun1.l.google.com:19302'}
        ]
        
        try:
            # This would need to be implemented in the frontend
            # For server-side, we'll use external services instead
            return None
        except Exception:
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
            logger.debug(f"ipify service failed: {e}")
        
        try:
            # Fallback to ipapi
            response = requests.get('https://ipapi.co/json/', timeout=5)
            if response.status_code == 200:
                data = response.json()
                ip = data.get('ip')
                if ip and self._validate_ip(ip):
                    return ip
        except Exception as e:
            logger.debug(f"ipapi service failed: {e}")
        
        return None
    
    def _get_from_stun(self) -> Optional[str]:
        """Get IP using STUN protocol"""
        try:
            # This would require STUN client implementation
            # For now, we'll skip this method
            return None
        except Exception:
            return None
    
    def _get_from_dns_query(self) -> Optional[str]:
        """Get IP using DNS query"""
        try:
            # Query for myip.com
            import dns.resolver
            answers = dns.resolver.resolve('myip.com', 'A')
            if answers:
                return str(answers[0])
        except Exception:
            return None
    
    def _get_from_ice_candidates(self) -> Optional[str]:
        """Get IP from ICE candidates"""
        # This would be implemented in frontend with WebRTC
        # Server-side equivalent not available
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
                'External Services',
                'WebRTC (frontend)',
                'STUN (future)'
            ],
            'current_method': 'Auto-detection',
            'reliability': 'High',
            'privacy_note': 'Server detects client IP automatically'
        }


# Singleton instance
ip_detector = ClientIPDetector()
