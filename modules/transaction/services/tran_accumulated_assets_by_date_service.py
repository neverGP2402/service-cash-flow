from typing import Optional
from datetime import datetime
from common.base.base_service import BaseService
from modules.transaction.repositories.tran_accumulated_assets_by_date_repository import TranAccumulatedAssetsByDateRepository
from modules.transaction.models.tran_accumulated_assets_by_date import TranAccumulatedAssetsByDate


class TranAccumulatedAssetsByDateService(BaseService):
    def __init__(self):
        repository = TranAccumulatedAssetsByDateRepository()
        super().__init__(repository)
        self.repository = repository

    def get_by_user_asset_date(self, user_id: int, asset_id: int, date: datetime) -> Optional[TranAccumulatedAssetsByDate]:
        return self.repository.find_by_user_asset_date(user_id, asset_id, date)
