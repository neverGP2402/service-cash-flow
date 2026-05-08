from typing import List, Optional
from common.base.base_repository import BaseRepository
from modules.transaction.models.tran_transactions import TranTransaction


class TranTransactionRepository(BaseRepository[TranTransaction]):
    def __init__(self):
        super().__init__(TranTransaction)

    def find_by_user_id(self, user_id: int, page: int = 1, limit: int = 10) -> List[TranTransaction]:
        return (
            self.session.query(TranTransaction)
            .filter(TranTransaction.user_id == user_id, TranTransaction.is_deleted.is_(False))
            .order_by(TranTransaction.date.desc())
            .offset((page - 1) * limit)
            .limit(limit)
            .all()
        )

    def count_by_user_id(self, user_id: int) -> int:
        return (
            self.session.query(TranTransaction)
            .filter(TranTransaction.user_id == user_id, TranTransaction.is_deleted.is_(False))
            .count()
        )
