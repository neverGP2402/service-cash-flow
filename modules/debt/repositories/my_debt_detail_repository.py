from typing import List
from common.base.base_repository import BaseRepository
from modules.debt.models.my_debt_detail import MyDebtDetail


class MyDebtDetailRepository(BaseRepository[MyDebtDetail]):
    def __init__(self):
        super().__init__(MyDebtDetail)

    def find_by_my_debt_id(self, my_debt_id: int) -> List[MyDebtDetail]:
        return (
            self.session.query(MyDebtDetail)
            .filter(MyDebtDetail.my_debt_id == my_debt_id, MyDebtDetail.is_deleted.is_(False))
            .order_by(MyDebtDetail.payment_date.desc())
            .all()
        )
