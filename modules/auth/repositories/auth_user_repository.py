from typing import Optional
from common.base.base_repository import BaseRepository
from modules.auth.models.auth_users import AuthUser


class AuthUserRepository(BaseRepository[AuthUser]):
    def __init__(self):
        super().__init__(AuthUser)

    def find_by_username(self, username: str) -> Optional[AuthUser]:
        return (
            self.session.query(AuthUser)
            .filter(AuthUser.username == username, AuthUser.is_deleted.is_(False))
            .first()
        )

    def find_by_email(self, email: str) -> Optional[AuthUser]:
        return (
            self.session.query(AuthUser)
            .filter(AuthUser.email == email, AuthUser.is_deleted.is_(False))
            .first()
        )
