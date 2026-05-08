from typing import Optional
from common.base.base_repository import BaseRepository
from modules.auth.models.authen_permission_screen import AuthenPermissionScreen


class AuthenPermissionScreenRepository(BaseRepository[AuthenPermissionScreen]):
    def __init__(self):
        super().__init__(AuthenPermissionScreen)

    def find_by_code(self, code: str) -> Optional[AuthenPermissionScreen]:
        return (
            self.session.query(AuthenPermissionScreen)
            .filter(AuthenPermissionScreen.code == code, AuthenPermissionScreen.is_deleted.is_(False))
            .first()
        )
