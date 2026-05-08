from common.utils.validate_util import require_field


class DebtReq:
    def __init__(self, data: dict):
        self.contract_no = data.get('contract_no')
        self.contract_date = data.get('contract_date')
        self.counterparty_id = data.get('counterparty_id')
        self.debt_type = data.get('debt_type')
        self.type = data.get('type')
        self.file_path_json = data.get('file_path_json')
        self.frequency = data.get('frequency')
        self.principal_debt = data.get('principal_debt', 0)
        self.interest = data.get('interest', 0)
        self.interest_rate = data.get('interest_rate', 0)
        self.insurance_fee = data.get('insurance_fee', 0)
        self.into_money = data.get('into_money', 0)
        self.paid_amount = data.get('paid_amount', 0)
        self.remaining_amount = data.get('remaining_amount', 0)
        self.cycle = data.get('cycle')
        self.paymented_times = data.get('paymented_times')
        self.start_date = data.get('start_date')
        self.exp_date = data.get('exp_date')
        self.status = data.get('status')
        self.description = data.get('description')
