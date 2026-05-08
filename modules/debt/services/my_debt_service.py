from typing import List, Optional
from common.base.base_service import BaseService
from modules.debt.repositories.my_debt_repository import MyDebtRepository
from modules.debt.models.my_debt import MyDebt


class MyDebtService(BaseService):
    def __init__(self):
        repository = MyDebtRepository()
        super().__init__(repository)
        self.debt_repository = repository

    def get_by_user_id(self, user_id: int, page: int = 1, limit: int = 10) -> List[MyDebt]:
        return self.debt_repository.find_by_user_id(user_id, page, limit)

    def get_by_contract_no(self, contract_no: str) -> Optional[MyDebt]:
        return self.debt_repository.find_by_contract_no(contract_no)
