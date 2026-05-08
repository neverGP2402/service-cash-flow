from typing import List
from common.base.base_service import BaseService
from modules.transaction.repositories.tran_notification_repository import TranNotificationRepository
from modules.transaction.models.tran_notification import TranNotification


class TranNotificationService(BaseService):
    def __init__(self):
        repository = TranNotificationRepository()
        super().__init__(repository)
        self.notification_repository = repository

    def get_by_user_id(self, user_id: int, page: int = 1, limit: int = 10) -> List[TranNotification]:
        return self.notification_repository.find_by_user_id(user_id, page, limit)

    def count_unread(self, user_id: int) -> int:
        return self.notification_repository.count_unread_by_user_id(user_id)
