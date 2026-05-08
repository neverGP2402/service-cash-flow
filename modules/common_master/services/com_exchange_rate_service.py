from typing import Optional
from common.base.base_service import BaseService
from modules.common_master.repositories.com_exchange_rate_repository import ComExchangeRateRepository
from modules.common_master.models.com_exchange_rate import ComExchangeRate


class ComExchangeRateService(BaseService):
    def __init__(self):
        repository = ComExchangeRateRepository()
        super().__init__(repository)
        self.repository = repository

    def get_by_asset_id(self, asset_id: int) -> Optional[ComExchangeRate]:
        return self.repository.find_by_asset_id(asset_id)
