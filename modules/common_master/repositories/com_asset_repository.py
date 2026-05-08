from typing import Optional
from common.base.base_repository import BaseRepository
from modules.common_master.models.com_asset import ComAsset


class ComAssetRepository(BaseRepository[ComAsset]):
    def __init__(self):
        super().__init__(ComAsset)

    def find_by_code(self, code: str) -> Optional[ComAsset]:
        return (
            self.session.query(ComAsset)
            .filter(ComAsset.code == code, ComAsset.is_deleted.is_(False))
            .first()
        )
