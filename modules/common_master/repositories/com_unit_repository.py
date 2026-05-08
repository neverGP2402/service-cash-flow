from typing import Optional
from common.base.base_repository import BaseRepository
from modules.common_master.models.com_unit import ComUnit


class ComUnitRepository(BaseRepository[ComUnit]):
    def __init__(self):
        super().__init__(ComUnit)

    def find_by_code(self, code: str) -> Optional[ComUnit]:
        return (
            self.session.query(ComUnit)
            .filter(ComUnit.code == code, ComUnit.is_deleted.is_(False))
            .first()
        )
