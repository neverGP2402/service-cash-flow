from typing import List
from common.base.base_repository import BaseRepository
from modules.asset.models.my_expense import MyExpense


class MyExpenseRepository(BaseRepository[MyExpense]):
    def __init__(self):
        super().__init__(MyExpense)

    def find_by_user_id(self, user_id: int, page: int = 1, limit: int = 10) -> List[MyExpense]:
        return (
            self.session.query(MyExpense)
            .filter(MyExpense.user_id == user_id, MyExpense.is_deleted.is_(False))
            .offset((page - 1) * limit)
            .limit(limit)
            .all()
        )
