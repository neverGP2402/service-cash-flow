from typing import List, Optional
from common.base.base_repository import BaseRepository
from modules.transaction.models.tran_result_by_month import TranResultByMonth


class TranResultByMonthRepository(BaseRepository[TranResultByMonth]):
    def __init__(self):
        super().__init__(TranResultByMonth)

    def find_by_user_month_year(self, user_id: int, month: int, year: int) -> Optional[TranResultByMonth]:
        return (
            self.session.query(TranResultByMonth)
            .filter(
                TranResultByMonth.user_id == user_id,
                TranResultByMonth.month == month,
                TranResultByMonth.year == year,
                TranResultByMonth.is_deleted.is_(False)
            )
            .first()
        )

    def find_by_user_id(self, user_id: int, page: int = 1, limit: int = 10) -> List[TranResultByMonth]:
        return (
            self.session.query(TranResultByMonth)
            .filter(TranResultByMonth.user_id == user_id, TranResultByMonth.is_deleted.is_(False))
            .order_by(TranResultByMonth.year.desc(), TranResultByMonth.month.desc())
            .offset((page - 1) * limit)
            .limit(limit)
            .all()
        )
