from flask import Blueprint, request, current_app
from common.base.base_controller import BaseController
from common.middlewares.auth_middleware import jwt_required_custom
from common.exceptions.app_exception import BadRequestException
from modules.auth.services.auth_service import AuthService
from modules.auth.services.sys_application_service import SysApplicationService
from modules.auth.services.sys_history_service import SysHistoryService
from modules.auth.services.auth_permission_service import AuthPermissionService
from modules.auth.services.social_auth_service import SocialAuthService
from modules.auth.models.sys_application import SysApplication
from modules.auth.models.sys_history import SysHistory
from modules.auth.models.auth_permission import AuthPermission
from modules.auth.models.authen_permission_screen import AuthenPermissionScreen
from modules.auth.models.authen_permission_screen_role import AuthenPermissionScreenRole
from modules.auth.validators.login_req import LoginReq
from modules.auth.validators.register_req import RegisterReq
from modules.auth.validators.social_login_req import SocialLoginReq
from modules.auth.utils.production_ip_detector import production_ip_detector

auth_bp = Blueprint('auth', __name__)


class AuthController(BaseController):
    def __init__(self):
        self.auth_service = AuthService()
        self.social_auth_service = SocialAuthService()
        self.application_service = SysApplicationService()
        self.history_service = SysHistoryService()
        self.permission_service = AuthPermissionService()

    def register(self):
        data = request.get_json(force=True)
        if not data:
            raise BadRequestException('Request body is required')
        register_req = RegisterReq(data)
        user = self.auth_service.register(register_req.to_dict())
        return self.created(data=user.to_dict(), message='User registered successfully')

    def login(self):
        """Login with username or email and password"""
        data = request.get_json(force=True)
        if not data:
            raise BadRequestException('Request body is required')
        LoginReq(data)
        
        # Support both username and email for login
        login_identifier = data.get('username')  # Can be username or email
        password = data.get('password')
        device_info = data.get('device_info', '')
        
        auto_detected_ip = production_ip_detector.detect_client_ip()
        ip_address = auto_detected_ip
        
        current_app.logger.info(f"Login auto-detected IP: {auto_detected_ip}")
        
        result = self.auth_service.login(login_identifier, password, device_info, ip_address)
        return self.ok(data=result, message='Login successful')

    def social_login(self):
        """Login with social providers (Google, GitHub, Facebook)"""
        data = request.get_json(force=True)
        if not data:
            raise BadRequestException('Request body is required')
        
        social_req = SocialLoginReq(data)
        
        # IP address handling - backend tự detect hoàn toàn
        social_data = social_req.to_dict()
        
        # Backend tự detect IP - client không cần truyền gì cả
        auto_detected_ip = ip_detector.detect_client_ip()
        social_data['ip_address'] = auto_detected_ip
        
        # Log IP detection (IPDetector tự log rồi, không cần log lại)
        # current_app.logger.info(f"Social login auto-detected IP: {auto_detected_ip}")
        
        result = self.social_auth_service.login_with_social(social_data)
        
        # Determine success message based on user creation
        message = 'Social login successful'
        if hasattr(result, 'get') and result.get('is_new_user', False):
            message = 'Account created successfully with social login'
        
        return self.ok(data=result, message=message)

    def _get_client_ip(self):
        """Get client IP address from multiple sources"""
        # Try different sources in order of reliability
        print("Headers:", request.headers)
        # 1. X-Forwarded-For header (when behind proxy)
        if request.headers.get('X-Forwarded-For'):
            ip = request.headers.get('X-Forwarded-For').split(',')[0].strip()
            return ip
        
        # 2. X-Real-IP header (when behind load balancer)
        if request.headers.get('X-Real-IP'):
            ip = request.headers.get('X-Real-IP')
            return ip
        
        # 3. X-Client-IP header
        if request.headers.get('X-Client-IP'):
            ip = request.headers.get('X-Client-IP')
            return ip
        
        # 4. CF-Connecting-IP header (Cloudflare)
        if request.headers.get('CF-Connecting-IP'):
            ip = request.headers.get('CF-Connecting-IP')
            return ip
        
        # 5. request.remote_addr (direct connection)
        if request.remote_addr:
            return request.remote_addr
        
        # 6. Fallback to localhost for development
        return 'Không lấy được IP'

    def logout(self):
        user_id = self._get_current_user_id()
        self.auth_service.logout(user_id)
        return self.ok(message='Logout successful')


auth_controller = AuthController()


@auth_bp.route('/register', methods=['POST'])
def register():
    return auth_controller.register()


@auth_bp.route('/login', methods=['POST'])
def login():
    return auth_controller.login()


@auth_bp.route('/social-login', methods=['POST'])
def social_login():
    return auth_controller.social_login()


@auth_bp.route('/logout', methods=['POST'])
@jwt_required_custom
def logout():
    return auth_controller.logout()
