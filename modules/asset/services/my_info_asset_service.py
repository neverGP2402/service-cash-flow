from typing import List, Optional
from common.base.base_service import BaseService
from modules.asset.repositories.my_info_asset_repository import MyInfoAssetRepository
from modules.asset.models.my_info_asset import MyInfoAsset


class MyInfoAssetService(BaseService):
    def __init__(self):
        repository = MyInfoAssetRepository()
        super().__init__(repository)
        self.repository = repository

    def get_by_user_id(self, user_id: int, page: int = 1, limit: int = 10) -> List[MyInfoAsset]:
        return self.repository.find_by_user_id(user_id, page, limit)

    def get_by_user_and_asset(self, user_id: int, asset_id: int) -> Optional[MyInfoAsset]:
        return self.repository.find_by_user_and_asset(user_id, asset_id)
