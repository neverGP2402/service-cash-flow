from typing import Optional
from common.base.base_repository import BaseRepository
from modules.common_master.models.com_counterparty import ComCounterparty


class ComCounterpartyRepository(BaseRepository[ComCounterparty]):
    def __init__(self):
        super().__init__(ComCounterparty)

    def find_by_code(self, code: str) -> Optional[ComCounterparty]:
        return (
            self.session.query(ComCounterparty)
            .filter(ComCounterparty.code == code, ComCounterparty.is_deleted.is_(False))
            .first()
        )
