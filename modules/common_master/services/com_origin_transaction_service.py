from typing import Optional
from common.base.base_service import BaseService
from modules.common_master.repositories.com_origin_transaction_repository import ComOriginTransactionRepository
from modules.common_master.models.com_origin_transaction import ComOriginTransaction


class ComOriginTransactionService(BaseService):
    def __init__(self):
        repository = ComOriginTransactionRepository()
        super().__init__(repository)
        self.repository = repository

    def get_by_code(self, code: str) -> Optional[ComOriginTransaction]:
        return self.repository.find_by_code(code)
