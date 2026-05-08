from common.base.base_repository import BaseRepository
from modules.auth.models.sys_application import SysApplication


class SysApplicationRepository(BaseRepository[SysApplication]):
    def __init__(self):
        super().__init__(SysApplication)
