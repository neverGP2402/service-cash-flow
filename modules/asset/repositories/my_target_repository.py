from typing import List
from common.base.base_repository import BaseRepository
from modules.asset.models.my_target import MyTarget


class MyTargetRepository(BaseRepository[MyTarget]):
    def __init__(self):
        super().__init__(MyTarget)

    def find_by_user_id(self, user_id: int, page: int = 1, limit: int = 10) -> List[MyTarget]:
        return (
            self.session.query(MyTarget)
            .filter(MyTarget.user_id == user_id, MyTarget.is_deleted.is_(False))
            .offset((page - 1) * limit)
            .limit(limit)
            .all()
        )
