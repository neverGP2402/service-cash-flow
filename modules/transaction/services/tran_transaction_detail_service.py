from typing import List
from common.base.base_service import BaseService
from modules.transaction.repositories.tran_transaction_detail_repository import TranTransactionDetailRepository
from modules.transaction.models.tran_transactions_detail import TranTransactionDetail


class TranTransactionDetailService(BaseService):
    def __init__(self):
        repository = TranTransactionDetailRepository()
        super().__init__(repository)
        self.detail_repository = repository

    def get_by_transaction_id(self, transaction_id: int) -> List[TranTransactionDetail]:
        return self.detail_repository.find_by_transaction_id(transaction_id)
