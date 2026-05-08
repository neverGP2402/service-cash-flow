from typing import List
from common.base.base_repository import BaseRepository
from modules.asset.models.my_target_plan import MyTargetPlan


class MyTargetPlanRepository(BaseRepository[MyTargetPlan]):
    def __init__(self):
        super().__init__(MyTargetPlan)

    def find_by_target_id(self, target_id: int) -> List[MyTargetPlan]:
        return (
            self.session.query(MyTargetPlan)
            .filter(MyTargetPlan.target_id == target_id, MyTargetPlan.is_deleted.is_(False))
            .order_by(MyTargetPlan.date.desc())
            .all()
        )
