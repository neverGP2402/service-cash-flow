from typing import Optional, List
from common.base.base_repository import BaseRepository
from modules.common_master.models.com_exchange_rate import ComExchangeRate


class ComExchangeRateRepository(BaseRepository[ComExchangeRate]):
    def __init__(self):
        super().__init__(ComExchangeRate)

    def find_by_asset_id(self, asset_id: int) -> Optional[ComExchangeRate]:
        return (
            self.session.query(ComExchangeRate)
            .filter(ComExchangeRate.asset_id == asset_id, ComExchangeRate.is_deleted.is_(False))
            .first()
        )
