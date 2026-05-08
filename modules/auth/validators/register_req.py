from common.utils.validate_util import require_field


class RegisterReq:
    def __init__(self, data: dict):
        self.username = require_field(data, 'username')
        self.email = require_field(data, 'email')
        self.password = require_field(data, 'password')
        self.full_name = data.get('full_name', '')
