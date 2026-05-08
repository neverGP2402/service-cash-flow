from common.utils.validate_util import require_field


class InfoAssetReq:
    def __init__(self, data: dict):
        self.asset_id = data.get('asset_id')
        self.wallet_id = data.get('wallet_id')
        self.amount = data.get('amount', 0)
        self.price = data.get('price', 0)
        self.origin = data.get('origin')
        self.status = data.get('status')
        self.description = data.get('description')
        self.unit_id = data.get('unit_id')
        self.transaction_date = data.get('transaction_date')
