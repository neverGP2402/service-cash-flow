from common.utils.validate_util import require_field


class TransactionReq:
    def __init__(self, data: dict):
        self.type = require_field(data, 'type')
        self.amount = require_field(data, 'amount')
        self.category_id = data.get('category_id')
        self.bill_image = data.get('bill_image')
        self.date = data.get('date')
        self.status = data.get('status')
        self.formality_transaction = data.get('formality_transaction')
        self.wallet_id = data.get('wallet_id')
        self.origin_transaction_id = data.get('origin_transaction_id')
        self.description = data.get('description')
        self.reference = data.get('reference')
        self.meta_data = data.get('meta_data')
