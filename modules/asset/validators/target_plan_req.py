from common.utils.validate_util import require_field


class TargetPlanReq:
    def __init__(self, data: dict):
        self.income = data.get('income', 0)
        self.expense = data.get('expense', 0)
        self.into_money_actual = data.get('into_money_actual', 0)
        self.date = data.get('date')
        self.status = data.get('status')
