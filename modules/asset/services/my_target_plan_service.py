from typing import List
from common.base.base_service import BaseService
from modules.asset.repositories.my_target_plan_repository import MyTargetPlanRepository
from modules.asset.models.my_target_plan import MyTargetPlan


class MyTargetPlanService(BaseService):
    def __init__(self):
        repository = MyTargetPlanRepository()
        super().__init__(repository)
        self.repository = repository

    def get_by_target_id(self, target_id: int) -> List[MyTargetPlan]:
        return self.repository.find_by_target_id(target_id)
