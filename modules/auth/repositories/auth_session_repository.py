from typing import Optional, List
from common.base.base_repository import BaseRepository
from modules.auth.models.auth_sessions import AuthSession


class AuthSessionRepository(BaseRepository[AuthSession]):
    def __init__(self):
        super().__init__(AuthSession)

    def find_by_token(self, token: str) -> Optional[AuthSession]:
        return (
            self.session.query(AuthSession)
            .filter(AuthSession.session_token == token, AuthSession.is_deleted.is_(False))
            .first()
        )

    def find_by_user_id(self, user_id: int) -> List[AuthSession]:
        return (
            self.session.query(AuthSession)
            .filter(AuthSession.user_id == user_id, AuthSession.is_deleted.is_(False))
            .all()
        )
