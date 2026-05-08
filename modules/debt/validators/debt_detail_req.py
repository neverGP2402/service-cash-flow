from common.utils.validate_util import require_field


class DebtDetailReq:
    def __init__(self, data: dict):
        self.principal_debt = data.get('principal_debt', 0)
        self.interest = data.get('interest', 0)
        self.insurance_fee = data.get('insurance_fee', 0)
        self.into_money = data.get('into_money', 0)
        self.paid_amount = data.get('paid_amount', 0)
        self.remaining_amount = data.get('remaining_amount', 0)
        self.payment_times = data.get('payment_times')
        self.payment_date = data.get('payment_date')
        self.payment_method = data.get('payment_method')
        self.transaction_id = data.get('transaction_id')
        self.wallet_id = data.get('wallet_id')
        self.bill_id = data.get('bill_id')
        self.status = data.get('status')
        self.description = data.get('description')
