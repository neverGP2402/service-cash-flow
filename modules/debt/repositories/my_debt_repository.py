from typing import List, Optional
from common.base.base_repository import BaseRepository
from modules.debt.models.my_debt import MyDebt


class MyDebtRepository(BaseRepository[MyDebt]):
    def __init__(self):
        super().__init__(MyDebt)

    def find_by_user_id(self, user_id: int, page: int = 1, limit: int = 10) -> List[MyDebt]:
        return (
            self.session.query(MyDebt)
            .filter(MyDebt.user_id == user_id, MyDebt.is_deleted.is_(False))
            .order_by(MyDebt.created_at.desc())
            .offset((page - 1) * limit)
            .limit(limit)
            .all()
        )

    def find_by_contract_no(self, contract_no: str) -> Optional[MyDebt]:
        return (
            self.session.query(MyDebt)
            .filter(MyDebt.contract_no == contract_no, MyDebt.is_deleted.is_(False))
            .first()
        )
