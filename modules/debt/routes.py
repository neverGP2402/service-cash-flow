from flask import Blueprint, request
from common.base.base_controller import BaseController
from common.middlewares.auth_middleware import jwt_required_custom, get_current_user_id
from common.exceptions.app_exception import BadRequestException
from modules.debt.services.my_debt_service import MyDebtService
from modules.debt.services.my_debt_detail_service import MyDebtDetailService
from modules.debt.models.my_debt import MyDebt
from modules.debt.models.my_debt_detail import MyDebtDetail
from modules.debt.validators.debt_req import DebtReq
from modules.debt.validators.debt_detail_req import DebtDetailReq

debt_bp = Blueprint('debt', __name__)


class DebtController(BaseController):
    def __init__(self):
        self.debt_service = MyDebtService()
        self.detail_service = MyDebtDetailService()

    def list_debts(self):
        user_id = get_current_user_id()
        params = self._get_pagination_params()
        filters = self._get_filter_params(['debt_type', 'type', 'status'])
        filters['user_id'] = user_id
        items = self.debt_service.get_all(filters=filters, page=params['page'], limit=params['limit'])
        total = self.debt_service.count(filters=filters)
        data = [i.to_dict() for i in items]
        return self.paginated(data=data, page=params['page'], limit=params['limit'], total=total)

    def get_debt(self, debt_id):
        item = self.debt_service.get_by_id(debt_id)
        if not item:
            return self.not_found('Debt not found')
        return self.ok(data=item.to_dict())

    def create_debt(self):
        data = request.get_json(force=True)
        if not data:
            raise BadRequestException('Request body is required')
        DebtReq(data)
        user_id = get_current_user_id()
        entity = MyDebt(
            user_id=user_id,
            contract_no=data.get('contract_no'),
            contract_date=data.get('contract_date'),
            counterparty_id=data.get('counterparty_id'),
            debt_type=data.get('debt_type'),
            type=data.get('type'),
            file_path_json=data.get('file_path_json'),
            frequency=data.get('frequency'),
            principal_debt=data.get('principal_debt', 0),
            interest=data.get('interest', 0),
            interest_rate=data.get('interest_rate', 0),
            insurance_fee=data.get('insurance_fee', 0),
            into_money=data.get('into_money', 0),
            paid_amount=data.get('paid_amount', 0),
            remaining_amount=data.get('remaining_amount', 0),
            cycle=data.get('cycle'),
            paymented_times=data.get('paymented_times'),
            start_date=data.get('start_date'),
            exp_date=data.get('exp_date'),
            status=data.get('status'),
            description=data.get('description'),
            created_by_user_id=user_id,
            updated_by_user_id=user_id
        )
        created = self.debt_service.create(entity)
        return self.created(data=created.to_dict())

    def update_debt(self, debt_id):
        data = request.get_json(force=True)
        if not data:
            raise BadRequestException('Request body is required')
        DebtReq(data)
        entity = self.debt_service.get_by_id(debt_id)
        if not entity:
            return self.not_found('Debt not found')
        for key, value in data.items():
            if hasattr(entity, key):
                setattr(entity, key, value)
        entity.updated_by_user_id = get_current_user_id()
        updated = self.debt_service.update(entity)
        return self.ok(data=updated.to_dict())

    def delete_debt(self, debt_id):
        user_id = get_current_user_id()
        success = self.debt_service.delete(debt_id, deleted_by_user_id=user_id)
        if not success:
            return self.not_found('Debt not found')
        return self.ok(message='Debt deleted')

    def list_details(self, debt_id):
        items = self.detail_service.get_by_my_debt_id(debt_id)
        data = [i.to_dict() for i in items]
        return self.ok(data=data)

    def create_detail(self, debt_id):
        data = request.get_json(force=True)
        DebtDetailReq(data)
        user_id = get_current_user_id()
        entity = MyDebtDetail(
            my_debt_id=debt_id,
            principal_debt=data.get('principal_debt', 0),
            interest=data.get('interest', 0),
            insurance_fee=data.get('insurance_fee', 0),
            into_money=data.get('into_money', 0),
            paid_amount=data.get('paid_amount', 0),
            remaining_amount=data.get('remaining_amount', 0),
            payment_times=data.get('payment_times'),
            payment_date=data.get('payment_date'),
            payment_method=data.get('payment_method'),
            transaction_id=data.get('transaction_id'),
            wallet_id=data.get('wallet_id'),
            bill_id=data.get('bill_id'),
            status=data.get('status'),
            description=data.get('description'),
            created_by_user_id=user_id,
            updated_by_user_id=user_id
        )
        created = self.detail_service.create(entity)
        return self.created(data=created.to_dict())

    def delete_detail(self, detail_id):
        user_id = get_current_user_id()
        success = self.detail_service.delete(detail_id, deleted_by_user_id=user_id)
        if not success:
            return self.not_found('Detail not found')
        return self.ok(message='Detail deleted')


debt_controller = DebtController()


@debt_bp.route('/debts', methods=['GET'])
@jwt_required_custom
def list_debts():
    return debt_controller.list_debts()


@debt_bp.route('/debts', methods=['POST'])
@jwt_required_custom
def create_debt():
    return debt_controller.create_debt()


@debt_bp.route('/debts/<int:debt_id>', methods=['GET'])
@jwt_required_custom
def get_debt(debt_id):
    return debt_controller.get_debt(debt_id)


@debt_bp.route('/debts/<int:debt_id>', methods=['PUT'])
@jwt_required_custom
def update_debt(debt_id):
    return debt_controller.update_debt(debt_id)


@debt_bp.route('/debts/<int:debt_id>', methods=['DELETE'])
@jwt_required_custom
def delete_debt(debt_id):
    return debt_controller.delete_debt(debt_id)


@debt_bp.route('/debts/<int:debt_id>/details', methods=['GET'])
@jwt_required_custom
def list_debt_details(debt_id):
    return debt_controller.list_details(debt_id)


@debt_bp.route('/debts/<int:debt_id>/details', methods=['POST'])
@jwt_required_custom
def create_debt_detail(debt_id):
    return debt_controller.create_detail(debt_id)


@debt_bp.route('/details/<int:detail_id>', methods=['DELETE'])
@jwt_required_custom
def delete_debt_detail(detail_id):
    return debt_controller.delete_detail(detail_id)
