from typing import Optional
from common.base.base_service import BaseService
from modules.common_master.repositories.com_counterparty_repository import ComCounterpartyRepository
from modules.common_master.models.com_counterparty import ComCounterparty


class ComCounterpartyService(BaseService):
    def __init__(self):
        repository = ComCounterpartyRepository()
        super().__init__(repository)
        self.repository = repository

    def get_by_code(self, code: str) -> Optional[ComCounterparty]:
        return self.repository.find_by_code(code)
