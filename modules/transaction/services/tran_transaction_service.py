from typing import List, Optional
from common.base.base_service import BaseService
from modules.transaction.repositories.tran_transaction_repository import TranTransactionRepository
from modules.transaction.models.tran_transactions import TranTransaction


class TranTransactionService(BaseService):
    def __init__(self):
        repository = TranTransactionRepository()
        super().__init__(repository)
        self.transaction_repository = repository

    def get_by_user_id(self, user_id: int, page: int = 1, limit: int = 10) -> List[TranTransaction]:
        return self.transaction_repository.find_by_user_id(user_id, page, limit)

    def count_by_user_id(self, user_id: int) -> int:
        return self.transaction_repository.count_by_user_id(user_id)
