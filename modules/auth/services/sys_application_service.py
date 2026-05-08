from common.base.base_service import BaseService
from modules.auth.repositories.sys_application_repository import SysApplicationRepository
from modules.auth.models.sys_application import SysApplication


class SysApplicationService(BaseService):
    def __init__(self):
        repository = SysApplicationRepository()
        super().__init__(repository)
