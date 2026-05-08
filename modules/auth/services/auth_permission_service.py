from common.base.base_service import BaseService
from modules.auth.repositories.auth_permission_repository import AuthPermissionRepository
from modules.auth.repositories.authen_permission_screen_repository import AuthenPermissionScreenRepository
from modules.auth.repositories.authen_permission_screen_role_repository import AuthenPermissionScreenRoleRepository
from modules.auth.models.auth_permission import AuthPermission
from modules.auth.models.authen_permission_screen import AuthenPermissionScreen
from modules.auth.models.authen_permission_screen_role import AuthenPermissionScreenRole


class AuthPermissionService(BaseService):
    def __init__(self):
        self.permission_repository = AuthPermissionRepository()
        self.screen_repository = AuthenPermissionScreenRepository()
        self.screen_role_repository = AuthenPermissionScreenRoleRepository()
        super().__init__(self.permission_repository)
