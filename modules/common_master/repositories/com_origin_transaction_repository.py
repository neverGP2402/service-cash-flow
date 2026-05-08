from typing import Optional
from common.base.base_repository import BaseRepository
from modules.common_master.models.com_origin_transaction import ComOriginTransaction


class ComOriginTransactionRepository(BaseRepository[ComOriginTransaction]):
    def __init__(self):
        super().__init__(ComOriginTransaction)

    def find_by_code(self, code: str) -> Optional[ComOriginTransaction]:
        return (
            self.session.query(ComOriginTransaction)
            .filter(ComOriginTransaction.code == code, ComOriginTransaction.is_deleted.is_(False))
            .first()
        )
