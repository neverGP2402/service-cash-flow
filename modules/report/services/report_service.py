from typing import List, Optional, Dict, Any
from common.base.base_service import BaseService
from modules.transaction.repositories.tran_transaction_repository import TranTransactionRepository
from modules.transaction.repositories.tran_result_by_month_repository import TranResultByMonthRepository
from config.logger import get_logger

logger = get_logger(__name__)


class ReportService(BaseService):
    def __init__(self):
        self.transaction_repository = TranTransactionRepository()
        self.result_repository = TranResultByMonthRepository()

    def get_monthly_summary(self, user_id: int, month: int, year: int) -> Dict[str, Any]:
        result = self.result_repository.find_by_user_month_year(user_id, month, year)
        if result:
            return result.to_dict()
        return {}

    def get_transaction_summary_by_type(self, user_id: int, month: int, year: int) -> Dict[str, float]:
        # Placeholder for actual aggregation logic
        return {'income': 0.0, 'expense': 0.0}
