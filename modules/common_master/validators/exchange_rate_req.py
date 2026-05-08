from common.utils.validate_util import require_field


class ExchangeRateReq:
    def __init__(self, data: dict):
        self.exchange_rate_purchase = data.get('exchange_rate_purchase', 0)
        self.exchange_rate_sell = data.get('exchange_rate_sell', 0)
        self.asset_id = require_field(data, 'asset_id')
        self.description = data.get('description')
        self.origin_info = data.get('origin_info')
