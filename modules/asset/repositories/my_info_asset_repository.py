from typing import List, Optional
from common.base.base_repository import BaseRepository
from modules.asset.models.my_info_asset import MyInfoAsset


class MyInfoAssetRepository(BaseRepository[MyInfoAsset]):
    def __init__(self):
        super().__init__(MyInfoAsset)

    def find_by_user_id(self, user_id: int, page: int = 1, limit: int = 10) -> List[MyInfoAsset]:
        return (
            self.session.query(MyInfoAsset)
            .filter(MyInfoAsset.user_id == user_id, MyInfoAsset.is_deleted.is_(False))
            .offset((page - 1) * limit)
            .limit(limit)
            .all()
        )

    def find_by_user_and_asset(self, user_id: int, asset_id: int) -> Optional[MyInfoAsset]:
        return (
            self.session.query(MyInfoAsset)
            .filter(
                MyInfoAsset.user_id == user_id,
                MyInfoAsset.asset_id == asset_id,
                MyInfoAsset.is_deleted.is_(False)
            )
            .first()
        )
