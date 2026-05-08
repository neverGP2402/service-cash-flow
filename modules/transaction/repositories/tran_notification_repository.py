from typing import List, Optional
from common.base.base_repository import BaseRepository
from modules.transaction.models.tran_notification import TranNotification


class TranNotificationRepository(BaseRepository[TranNotification]):
    def __init__(self):
        super().__init__(TranNotification)

    def find_by_user_id(self, user_id: int, page: int = 1, limit: int = 10) -> List[TranNotification]:
        return (
            self.session.query(TranNotification)
            .filter(TranNotification.user_id == user_id, TranNotification.is_deleted.is_(False))
            .order_by(TranNotification.created_at.desc())
            .offset((page - 1) * limit)
            .limit(limit)
            .all()
        )

    def count_unread_by_user_id(self, user_id: int) -> int:
        return (
            self.session.query(TranNotification)
            .filter(
                TranNotification.user_id == user_id,
                TranNotification.is_read.is_(False),
                TranNotification.is_deleted.is_(False)
            )
            .count()
        )
