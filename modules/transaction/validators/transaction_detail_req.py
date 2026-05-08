from common.utils.validate_util import require_field


class TransactionDetailReq:
    def __init__(self, data: dict):
        self.product_name = data.get('product_name')
        self.amount = data.get('amount', 0)
        self.price = data.get('price', 0)
        self.into_money = data.get('into_money', 0)
        self.date = data.get('date')
        self.description = data.get('description')
