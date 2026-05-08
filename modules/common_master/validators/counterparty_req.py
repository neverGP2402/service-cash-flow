from common.utils.validate_util import require_field


class CounterpartyReq:
    def __init__(self, data: dict):
        self.code = require_field(data, 'code')
        self.name = require_field(data, 'name')
        self.phone = data.get('phone')
        self.avatar = data.get('avatar')
