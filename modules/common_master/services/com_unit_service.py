from typing import Optional
from common.base.base_service import BaseService
from modules.common_master.repositories.com_unit_repository import ComUnitRepository
from modules.common_master.models.com_unit import ComUnit


class ComUnitService(BaseService):
    def __init__(self):
        repository = ComUnitRepository()
        super().__init__(repository)
        self.repository = repository

    def get_by_code(self, code: str) -> Optional[ComUnit]:
        return self.repository.find_by_code(code)
