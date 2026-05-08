from typing import Optional
from common.base.base_service import BaseService
from modules.common_master.repositories.com_category_repository import ComCategoryRepository
from modules.common_master.models.com_categories import ComCategory


class ComCategoryService(BaseService):
    def __init__(self):
        repository = ComCategoryRepository()
        super().__init__(repository)
        self.repository = repository

    def get_by_code(self, code: str) -> Optional[ComCategory]:
        return self.repository.find_by_code(code)
