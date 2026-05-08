from typing import List, Optional
from common.base.base_service import BaseService
from modules.transaction.repositories.tran_result_by_month_repository import TranResultByMonthRepository
from modules.transaction.models.tran_result_by_month import TranResultByMonth


class TranResultByMonthService(BaseService):
    def __init__(self):
        repository = TranResultByMonthRepository()
        super().__init__(repository)
        self.repository = repository

    def get_by_user_month_year(self, user_id: int, month: int, year: int) -> Optional[TranResultByMonth]:
        return self.repository.find_by_user_month_year(user_id, month, year)

    def get_by_user_id(self, user_id: int, page: int = 1, limit: int = 10) -> List[TranResultByMonth]:
        return self.repository.find_by_user_id(user_id, page, limit)
