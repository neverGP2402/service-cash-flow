from typing import List
from common.base.base_repository import BaseRepository
from modules.auth.models.authen_permission_screen_role import AuthenPermissionScreenRole


class AuthenPermissionScreenRoleRepository(BaseRepository[AuthenPermissionScreenRole]):
    def __init__(self):
        super().__init__(AuthenPermissionScreenRole)

    def find_by_permission_id(self, permission_id: int) -> List[AuthenPermissionScreenRole]:
        return (
            self.session.query(AuthenPermissionScreenRole)
            .filter(
                AuthenPermissionScreenRole.permission_id == permission_id,
                AuthenPermissionScreenRole.is_deleted.is_(False)
            )
            .all()
        )

    def find_by_screen_id(self, screen_id: int) -> List[AuthenPermissionScreenRole]:
        return (
            self.session.query(AuthenPermissionScreenRole)
            .filter(
                AuthenPermissionScreenRole.permission_screen_id == screen_id,
                AuthenPermissionScreenRole.is_deleted.is_(False)
            )
            .all()
        )
