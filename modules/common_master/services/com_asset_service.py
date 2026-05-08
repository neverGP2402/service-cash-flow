from typing import Optional
from common.base.base_service import BaseService
from modules.common_master.repositories.com_asset_repository import ComAssetRepository
from modules.common_master.models.com_asset import ComAsset


class ComAssetService(BaseService):
    def __init__(self):
        repository = ComAssetRepository()
        super().__init__(repository)
        self.repository = repository

    def get_by_code(self, code: str) -> Optional[ComAsset]:
        return self.repository.find_by_code(code)
