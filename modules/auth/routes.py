from flask import Blueprint, request
from common.base.base_controller import BaseController
from common.middlewares.auth_middleware import jwt_required_custom
from common.exceptions.app_exception import BadRequestException
from modules.auth.services.auth_service import AuthService
from modules.auth.services.sys_application_service import SysApplicationService
from modules.auth.services.sys_history_service import SysHistoryService
from modules.auth.services.auth_permission_service import AuthPermissionService
from modules.auth.models.sys_application import SysApplication
from modules.auth.models.sys_history import SysHistory
from modules.auth.models.auth_permission import AuthPermission
from modules.auth.models.authen_permission_screen import AuthenPermissionScreen
from modules.auth.models.authen_permission_screen_role import AuthenPermissionScreenRole
from modules.auth.validators.login_req import LoginReq
from modules.auth.validators.register_req import RegisterReq

auth_bp = Blueprint('auth', __name__)


class AuthController(BaseController):
    def __init__(self):
        self.auth_service = AuthService()
        self.application_service = SysApplicationService()
        self.history_service = SysHistoryService()
        self.permission_service = AuthPermissionService()

    def register(self):
        data = request.get_json(force=True)
        if not data:
            raise BadRequestException('Request body is required')
        RegisterReq(data)
        user = self.auth_service.register(data)
        return self.created(data=user.to_dict(), message='User registered successfully')

    def login(self):
        data = request.get_json(force=True)
        if not data:
            raise BadRequestException('Request body is required')
        LoginReq(data)
        username = data.get('username')
        password = data.get('password')
        device_info = data.get('device_info', '')
        ip_address = request.remote_addr or ''
        result = self.auth_service.login(username, password, device_info, ip_address)
        return self.ok(data=result, message='Login successful')

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


@auth_bp.route('/logout', methods=['POST'])
@jwt_required_custom
def logout():
    return auth_controller.logout()
