from common.utils.validate_util import require_field


class TargetReq:
    def __init__(self, data: dict):
        self.name = require_field(data, 'name')
        self.income = data.get('income', 0)
        self.expense = data.get('expense', 0)
        self.description = data.get('description')
        self.time_cycle = data.get('time_cycle', 0)
        self.type = data.get('type')
        self.progress = data.get('progress', 0)
        self.status = data.get('status')
        self.setting_date = data.get('setting_date')
        self.effective_date = data.get('effective_date')
