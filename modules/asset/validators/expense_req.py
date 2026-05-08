from common.utils.validate_util import require_field


class ExpenseReq:
    def __init__(self, data: dict):
        self.expense_id = data.get('expense_id')
        self.type = data.get('type')
        self.frequency = data.get('frequency')
        self.amount = data.get('amount', 0)
        self.price = data.get('price', 0)
        self.into_money = data.get('into_money', 0)
        self.effective_date = data.get('effective_date')
        self.exp_date = data.get('exp_date')
        self.status = data.get('status')
        self.description = data.get('description')
