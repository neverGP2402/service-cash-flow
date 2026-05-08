from typing import Optional
from modules.common_master.repositories.com_exchange_rate_repository import ComExchangeRateRepository
from modules.common_master.models.com_exchange_rate import ComExchangeRate
from config.logger import get_logger

logger = get_logger(__name__)


class ExchangeRateService:
    def __init__(self):
        self.repository = ComExchangeRateRepository()

    def get_by_asset_id(self, asset_id: int) -> Optional[ComExchangeRate]:
        return self.repository.find_by_asset_id(asset_id)

    def update_rate(self, asset_id: int, purchase: float, sell: float, origin_info: str) -> ComExchangeRate:
        existing = self.repository.find_by_asset_id(asset_id)
        if existing:
            existing.exchange_rate_purchase = purchase
            existing.exchange_rate_sell = sell
            existing.origin_info = origin_info
            return self.repository.update(existing)
        entity = ComExchangeRate(
            asset_id=asset_id,
            exchange_rate_purchase=purchase,
            exchange_rate_sell=sell,
            origin_info=origin_info
        )
        return self.repository.create(entity)
