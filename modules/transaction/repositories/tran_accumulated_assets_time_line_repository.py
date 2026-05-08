from typing import List, Optional
from common.base.base_repository import BaseRepository
from modules.transaction.models.tran_accumulated_assets_time_line import TranAccumulatedAssetsTimeLine


class TranAccumulatedAssetsTimeLineRepository(BaseRepository[TranAccumulatedAssetsTimeLine]):
    def __init__(self):
        super().__init__(TranAccumulatedAssetsTimeLine)

    def find_by_user_and_asset(self, user_id: int, asset_id: int) -> List[TranAccumulatedAssetsTimeLine]:
        return (
            self.session.query(TranAccumulatedAssetsTimeLine)
            .filter(
                TranAccumulatedAssetsTimeLine.user_id == user_id,
                TranAccumulatedAssetsTimeLine.asset_id == asset_id,
                TranAccumulatedAssetsTimeLine.is_deleted.is_(False)
            )
            .order_by(TranAccumulatedAssetsTimeLine.created_at.desc())
            .all()
        )
