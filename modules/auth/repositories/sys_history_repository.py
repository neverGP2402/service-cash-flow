from common.base.base_repository import BaseRepository
from modules.auth.models.sys_history import SysHistory


class SysHistoryRepository(BaseRepository[SysHistory]):
    def __init__(self):
        super().__init__(SysHistory)
