from typing import List, Optional
from datetime import datetime
from common.base.base_repository import BaseRepository
from modules.transaction.models.tran_accumulated_assets_by_date import TranAccumulatedAssetsByDate


class TranAccumulatedAssetsByDateRepository(BaseRepository[TranAccumulatedAssetsByDate]):
    def __init__(self):
        super().__init__(TranAccumulatedAssetsByDate)

    def find_by_user_asset_date(self, user_id: int, asset_id: int, date: datetime) -> Optional[TranAccumulatedAssetsByDate]:
        return (
            self.session.query(TranAccumulatedAssetsByDate)
            .filter(
                TranAccumulatedAssetsByDate.user_id == user_id,
                TranAccumulatedAssetsByDate.asset_id == asset_id,
                TranAccumulatedAssetsByDate.date == date,
                TranAccumulatedAssetsByDate.is_deleted.is_(False)
            )
            .first()
        )
