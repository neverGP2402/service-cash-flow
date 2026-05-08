from typing import List
from common.base.base_service import BaseService
from modules.debt.repositories.my_debt_detail_repository import MyDebtDetailRepository
from modules.debt.models.my_debt_detail import MyDebtDetail


class MyDebtDetailService(BaseService):
    def __init__(self):
        repository = MyDebtDetailRepository()
        super().__init__(repository)
        self.detail_repository = repository

    def get_by_my_debt_id(self, my_debt_id: int) -> List[MyDebtDetail]:
        return self.detail_repository.find_by_my_debt_id(my_debt_id)
