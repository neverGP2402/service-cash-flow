from flask import Blueprint, request
from common.base.base_controller import BaseController
from common.middlewares.auth_middleware import jwt_required_custom, get_current_user_id
from modules.report.services.report_service import ReportService

report_bp = Blueprint('report', __name__)


class ReportController(BaseController):
    def __init__(self):
        self.report_service = ReportService()

    def monthly_summary(self):
        user_id = get_current_user_id()
        month = request.args.get('month', type=int)
        year = request.args.get('year', type=int)
        if not month or not year:
            return self.bad_request('month and year are required')
        data = self.report_service.get_monthly_summary(user_id, month, year)
        return self.ok(data=data)

    def transaction_summary(self):
        user_id = get_current_user_id()
        month = request.args.get('month', type=int)
        year = request.args.get('year', type=int)
        if not month or not year:
            return self.bad_request('month and year are required')
        data = self.report_service.get_transaction_summary_by_type(user_id, month, year)
        return self.ok(data=data)


report_controller = ReportController()


@report_bp.route('/monthly-summary', methods=['GET'])
@jwt_required_custom
def monthly_summary():
    return report_controller.monthly_summary()


@report_bp.route('/transaction-summary', methods=['GET'])
@jwt_required_custom
def transaction_summary():
    return report_controller.transaction_summary()
