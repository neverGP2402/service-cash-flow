from common.utils.validate_util import require_field


class AssetReq:
    def __init__(self, data: dict):
        self.code = require_field(data, 'code')
        self.name = require_field(data, 'name')
        self.type = data.get('type')
        self.unit_id = data.get('unit_id')
