from typing import List, Optional
from common.base.base_service import BaseService
from modules.common_master.repositories.com_wallet_repository import ComWalletRepository
from modules.common_master.models.com_wallets import ComWallet


class ComWalletService(BaseService):
    def __init__(self):
        repository = ComWalletRepository()
        super().__init__(repository)
        self.repository = repository

    def get_by_user_id(self, user_id: int, page: int = 1, limit: int = 10) -> List[ComWallet]:
        return self.repository.find_by_user_id(user_id, page, limit)

    def get_by_code(self, code: str) -> Optional[ComWallet]:
        return self.repository.find_by_code(code)
