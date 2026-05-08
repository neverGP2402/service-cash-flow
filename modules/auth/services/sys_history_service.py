from common.base.base_service import BaseService
from modules.auth.repositories.sys_history_repository import SysHistoryRepository
from modules.auth.models.sys_history import SysHistory


class SysHistoryService(BaseService):
    def __init__(self):
        repository = SysHistoryRepository()
        super().__init__(repository)
