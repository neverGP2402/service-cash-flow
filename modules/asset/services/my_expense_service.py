from typing import List
from common.base.base_service import BaseService
from modules.asset.repositories.my_expense_repository import MyExpenseRepository
from modules.asset.models.my_expense import MyExpense


class MyExpenseService(BaseService):
    def __init__(self):
        repository = MyExpenseRepository()
        super().__init__(repository)
        self.repository = repository

    def get_by_user_id(self, user_id: int, page: int = 1, limit: int = 10) -> List[MyExpense]:
        return self.repository.find_by_user_id(user_id, page, limit)
