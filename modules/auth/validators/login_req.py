from common.exceptions.validate_exception import ValidationException
from common.utils.validate_util import require_field


class LoginReq:
    def __init__(self, data: dict):
        self.username = require_field(data, 'username')
        self.password = require_field(data, 'password')
