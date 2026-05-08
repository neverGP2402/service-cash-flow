from typing import List
from common.base.base_repository import BaseRepository
from modules.transaction.models.tran_transactions_detail import TranTransactionDetail


class TranTransactionDetailRepository(BaseRepository[TranTransactionDetail]):
    def __init__(self):
        super().__init__(TranTransactionDetail)

    def find_by_transaction_id(self, transaction_id: int) -> List[TranTransactionDetail]:
        return (
            self.session.query(TranTransactionDetail)
            .filter(
                TranTransactionDetail.transaction_id == transaction_id,
                TranTransactionDetail.is_deleted.is_(False)
            )
            .all()
        )
