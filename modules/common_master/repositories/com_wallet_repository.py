from typing import List, Optional
from common.base.base_repository import BaseRepository
from modules.common_master.models.com_wallets import ComWallet


class ComWalletRepository(BaseRepository[ComWallet]):
    def __init__(self):
        super().__init__(ComWallet)

    def find_by_user_id(self, user_id: int, page: int = 1, limit: int = 10) -> List[ComWallet]:
        return (
            self.session.query(ComWallet)
            .filter(ComWallet.user_id == user_id, ComWallet.is_deleted.is_(False))
            .offset((page - 1) * limit)
            .limit(limit)
            .all()
        )

    def find_by_code(self, code: str) -> Optional[ComWallet]:
        return (
            self.session.query(ComWallet)
            .filter(ComWallet.code == code, ComWallet.is_deleted.is_(False))
            .first()
        )
