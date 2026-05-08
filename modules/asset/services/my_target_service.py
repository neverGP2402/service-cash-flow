from typing import List
from common.base.base_service import BaseService
from modules.asset.repositories.my_target_repository import MyTargetRepository
from modules.asset.models.my_target import MyTarget


class MyTargetService(BaseService):
    def __init__(self):
        repository = MyTargetRepository()
        super().__init__(repository)
        self.repository = repository

    def get_by_user_id(self, user_id: int, page: int = 1, limit: int = 10) -> List[MyTarget]:
        return self.repository.find_by_user_id(user_id, page, limit)
