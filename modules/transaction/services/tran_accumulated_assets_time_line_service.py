from typing import List
from common.base.base_service import BaseService
from modules.transaction.repositories.tran_accumulated_assets_time_line_repository import TranAccumulatedAssetsTimeLineRepository
from modules.transaction.models.tran_accumulated_assets_time_line import TranAccumulatedAssetsTimeLine


class TranAccumulatedAssetsTimeLineService(BaseService):
    def __init__(self):
        repository = TranAccumulatedAssetsTimeLineRepository()
        super().__init__(repository)
        self.repository = repository

    def get_by_user_and_asset(self, user_id: int, asset_id: int) -> List[TranAccumulatedAssetsTimeLine]:
        return self.repository.find_by_user_and_asset(user_id, asset_id)
