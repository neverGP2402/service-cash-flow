from common.utils.validate_util import require_field


class NotificationReq:
    def __init__(self, data: dict):
        self.title = require_field(data, 'title')
        self.content = data.get('content')
        self.type = data.get('type')
        self.status = data.get('status')
        self.sent_at = data.get('sent_at')
        self.is_read = data.get('is_read', False)
        self.read_at = data.get('read_at')
        self.priority = data.get('priority')
