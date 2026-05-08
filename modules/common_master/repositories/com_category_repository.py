from typing import Optional
from common.base.base_repository import BaseRepository
from modules.common_master.models.com_categories import ComCategory


class ComCategoryRepository(BaseRepository[ComCategory]):
    def __init__(self):
        super().__init__(ComCategory)

    def find_by_code(self, code: str) -> Optional[ComCategory]:
        return (
            self.session.query(ComCategory)
            .filter(ComCategory.code == code, ComCategory.is_deleted.is_(False))
            .first()
        )
