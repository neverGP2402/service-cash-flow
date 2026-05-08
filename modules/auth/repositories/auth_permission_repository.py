from typing import Optional
from common.base.base_repository import BaseRepository
from modules.auth.models.auth_permission import AuthPermission


class AuthPermissionRepository(BaseRepository[AuthPermission]):
    def __init__(self):
        super().__init__(AuthPermission)

    def find_by_code(self, code: str) -> Optional[AuthPermission]:
        return (
            self.session.query(AuthPermission)
            .filter(AuthPermission.code == code, AuthPermission.is_deleted.is_(False))
            .first()
        )
