from flask import Blueprint, request
from common.base.base_controller import BaseController
from common.middlewares.auth_middleware import jwt_required_custom, get_current_user_id
from common.exceptions.app_exception import BadRequestException
from modules.asset.services.my_info_asset_service import MyInfoAssetService
from modules.asset.services.my_target_service import MyTargetService
from modules.asset.services.my_target_plan_service import MyTargetPlanService
from modules.asset.services.my_expense_service import MyExpenseService
from modules.asset.models.my_info_asset import MyInfoAsset
from modules.asset.models.my_target import MyTarget
from modules.asset.models.my_target_plan import MyTargetPlan
from modules.asset.models.my_expense import MyExpense
from modules.asset.validators.info_asset_req import InfoAssetReq
from modules.asset.validators.target_req import TargetReq
from modules.asset.validators.target_plan_req import TargetPlanReq
from modules.asset.validators.expense_req import ExpenseReq

asset_bp = Blueprint('asset', __name__)


class AssetController(BaseController):
    def __init__(self):
        self.info_asset_service = MyInfoAssetService()
        self.target_service = MyTargetService()
        self.target_plan_service = MyTargetPlanService()
        self.expense_service = MyExpenseService()

    # MyInfoAsset
    def list_info_assets(self):
        user_id = get_current_user_id()
        params = self._get_pagination_params()
        filters = self._get_filter_params(['asset_id', 'status'])
        filters['user_id'] = user_id
        items = self.info_asset_service.get_all(filters=filters, page=params['page'], limit=params['limit'])
        total = self.info_asset_service.count(filters=filters)
        data = [i.to_dict() for i in items]
        return self.paginated(data=data, page=params['page'], limit=params['limit'], total=total)

    def get_info_asset(self, asset_info_id):
        item = self.info_asset_service.get_by_id(asset_info_id)
        if not item:
            return self.not_found('Asset info not found')
        return self.ok(data=item.to_dict())

    def create_info_asset(self):
        data = request.get_json(force=True)
        if not data:
            raise BadRequestException('Request body is required')
        InfoAssetReq(data)
        user_id = get_current_user_id()
        entity = MyInfoAsset(
            user_id=user_id,
            asset_id=data.get('asset_id'),
            wallet_id=data.get('wallet_id'),
            amount=data.get('amount', 0),
            price=data.get('price', 0),
            origin=data.get('origin'),
            status=data.get('status'),
            description=data.get('description'),
            unit_id=data.get('unit_id'),
            transaction_date=data.get('transaction_date'),
            created_by_user_id=user_id,
            updated_by_user_id=user_id
        )
        created = self.info_asset_service.create(entity)
        return self.created(data=created.to_dict())

    def update_info_asset(self, asset_info_id):
        data = request.get_json(force=True)
        if not data:
            raise BadRequestException('Request body is required')
        InfoAssetReq(data)
        entity = self.info_asset_service.get_by_id(asset_info_id)
        if not entity:
            return self.not_found('Asset info not found')
        for key, value in data.items():
            if hasattr(entity, key):
                setattr(entity, key, value)
        entity.updated_by_user_id = get_current_user_id()
        updated = self.info_asset_service.update(entity)
        return self.ok(data=updated.to_dict())

    def delete_info_asset(self, asset_info_id):
        user_id = get_current_user_id()
        success = self.info_asset_service.delete(asset_info_id, deleted_by_user_id=user_id)
        if not success:
            return self.not_found('Asset info not found')
        return self.ok(message='Asset info deleted')

    # MyTarget
    def list_targets(self):
        user_id = get_current_user_id()
        params = self._get_pagination_params()
        items = self.target_service.get_by_user_id(user_id, params['page'], params['limit'])
        data = [i.to_dict() for i in items]
        return self.ok(data=data)

    def get_target(self, target_id):
        item = self.target_service.get_by_id(target_id)
        if not item:
            return self.not_found('Target not found')
        return self.ok(data=item.to_dict())

    def create_target(self):
        data = request.get_json(force=True)
        if not data:
            raise BadRequestException('Request body is required')
        TargetReq(data)
        user_id = get_current_user_id()
        entity = MyTarget(
            user_id=user_id,
            name=data.get('name'),
            income=data.get('income', 0),
            expense=data.get('expense', 0),
            description=data.get('description'),
            time_cycle=data.get('time_cycle', 0),
            type=data.get('type'),
            progress=data.get('progress', 0),
            status=data.get('status'),
            setting_date=data.get('setting_date'),
            effective_date=data.get('effective_date'),
            created_by_user_id=user_id,
            updated_by_user_id=user_id
        )
        created = self.target_service.create(entity)
        return self.created(data=created.to_dict())

    def update_target(self, target_id):
        data = request.get_json(force=True)
        if not data:
            raise BadRequestException('Request body is required')
        TargetReq(data)
        entity = self.target_service.get_by_id(target_id)
        if not entity:
            return self.not_found('Target not found')
        for key, value in data.items():
            if hasattr(entity, key):
                setattr(entity, key, value)
        entity.updated_by_user_id = get_current_user_id()
        updated = self.target_service.update(entity)
        return self.ok(data=updated.to_dict())

    def delete_target(self, target_id):
        user_id = get_current_user_id()
        success = self.target_service.delete(target_id, deleted_by_user_id=user_id)
        if not success:
            return self.not_found('Target not found')
        return self.ok(message='Target deleted')

    # MyTargetPlan
    def list_target_plans(self, target_id):
        items = self.target_plan_service.get_by_target_id(target_id)
        data = [i.to_dict() for i in items]
        return self.ok(data=data)

    def create_target_plan(self, target_id):
        data = request.get_json(force=True)
        if not data:
            raise BadRequestException('Request body is required')
        TargetPlanReq(data)
        user_id = get_current_user_id()
        entity = MyTargetPlan(
            user_id=user_id,
            target_id=target_id,
            income=data.get('income', 0),
            expense=data.get('expense', 0),
            into_money_actual=data.get('into_money_actual', 0),
            date=data.get('date'),
            status=data.get('status'),
            created_by_user_id=user_id,
            updated_by_user_id=user_id
        )
        created = self.target_plan_service.create(entity)
        return self.created(data=created.to_dict())

    def delete_target_plan(self, plan_id):
        user_id = get_current_user_id()
        success = self.target_plan_service.delete(plan_id, deleted_by_user_id=user_id)
        if not success:
            return self.not_found('Plan not found')
        return self.ok(message='Plan deleted')

    # MyExpense
    def list_expenses(self):
        user_id = get_current_user_id()
        params = self._get_pagination_params()
        items = self.expense_service.get_by_user_id(user_id, params['page'], params['limit'])
        data = [i.to_dict() for i in items]
        return self.ok(data=data)

    def get_expense(self, expense_id):
        item = self.expense_service.get_by_id(expense_id)
        if not item:
            return self.not_found('Expense not found')
        return self.ok(data=item.to_dict())

    def create_expense(self):
        data = request.get_json(force=True)
        if not data:
            raise BadRequestException('Request body is required')
        ExpenseReq(data)
        user_id = get_current_user_id()
        entity = MyExpense(
            user_id=user_id,
            expense_id=data.get('expense_id'),
            type=data.get('type'),
            frequency=data.get('frequency'),
            amount=data.get('amount', 0),
            price=data.get('price', 0),
            into_money=data.get('into_money', 0),
            effective_date=data.get('effective_date'),
            exp_date=data.get('exp_date'),
            status=data.get('status'),
            description=data.get('description'),
            created_by_user_id=user_id,
            updated_by_user_id=user_id
        )
        created = self.expense_service.create(entity)
        return self.created(data=created.to_dict())

    def update_expense(self, expense_id):
        data = request.get_json(force=True)
        if not data:
            raise BadRequestException('Request body is required')
        ExpenseReq(data)
        entity = self.expense_service.get_by_id(expense_id)
        if not entity:
            return self.not_found('Expense not found')
        for key, value in data.items():
            if hasattr(entity, key):
                setattr(entity, key, value)
        entity.updated_by_user_id = get_current_user_id()
        updated = self.expense_service.update(entity)
        return self.ok(data=updated.to_dict())

    def delete_expense(self, expense_id):
        user_id = get_current_user_id()
        success = self.expense_service.delete(expense_id, deleted_by_user_id=user_id)
        if not success:
            return self.not_found('Expense not found')
        return self.ok(message='Expense deleted')


asset_controller = AssetController()


# MyInfoAsset routes
@asset_bp.route('/info-assets', methods=['GET'])
@jwt_required_custom
def list_info_assets():
    return asset_controller.list_info_assets()


@asset_bp.route('/info-assets', methods=['POST'])
@jwt_required_custom
def create_info_asset():
    return asset_controller.create_info_asset()


@asset_bp.route('/info-assets/<int:asset_info_id>', methods=['GET'])
@jwt_required_custom
def get_info_asset(asset_info_id):
    return asset_controller.get_info_asset(asset_info_id)


@asset_bp.route('/info-assets/<int:asset_info_id>', methods=['PUT'])
@jwt_required_custom
def update_info_asset(asset_info_id):
    return asset_controller.update_info_asset(asset_info_id)


@asset_bp.route('/info-assets/<int:asset_info_id>', methods=['DELETE'])
@jwt_required_custom
def delete_info_asset(asset_info_id):
    return asset_controller.delete_info_asset(asset_info_id)


# MyTarget routes
@asset_bp.route('/targets', methods=['GET'])
@jwt_required_custom
def list_targets():
    return asset_controller.list_targets()


@asset_bp.route('/targets', methods=['POST'])
@jwt_required_custom
def create_target():
    return asset_controller.create_target()


@asset_bp.route('/targets/<int:target_id>', methods=['GET'])
@jwt_required_custom
def get_target(target_id):
    return asset_controller.get_target(target_id)


@asset_bp.route('/targets/<int:target_id>', methods=['PUT'])
@jwt_required_custom
def update_target(target_id):
    return asset_controller.update_target(target_id)


@asset_bp.route('/targets/<int:target_id>', methods=['DELETE'])
@jwt_required_custom
def delete_target(target_id):
    return asset_controller.delete_target(target_id)


# MyTargetPlan routes
@asset_bp.route('/targets/<int:target_id>/plans', methods=['GET'])
@jwt_required_custom
def list_target_plans(target_id):
    return asset_controller.list_target_plans(target_id)


@asset_bp.route('/targets/<int:target_id>/plans', methods=['POST'])
@jwt_required_custom
def create_target_plan(target_id):
    return asset_controller.create_target_plan(target_id)


@asset_bp.route('/plans/<int:plan_id>', methods=['DELETE'])
@jwt_required_custom
def delete_target_plan(plan_id):
    return asset_controller.delete_target_plan(plan_id)


# MyExpense routes
@asset_bp.route('/expenses', methods=['GET'])
@jwt_required_custom
def list_expenses():
    return asset_controller.list_expenses()


@asset_bp.route('/expenses', methods=['POST'])
@jwt_required_custom
def create_expense():
    return asset_controller.create_expense()


@asset_bp.route('/expenses/<int:expense_id>', methods=['GET'])
@jwt_required_custom
def get_expense(expense_id):
    return asset_controller.get_expense(expense_id)


@asset_bp.route('/expenses/<int:expense_id>', methods=['PUT'])
@jwt_required_custom
def update_expense(expense_id):
    return asset_controller.update_expense(expense_id)


@asset_bp.route('/expenses/<int:expense_id>', methods=['DELETE'])
@jwt_required_custom
def delete_expense(expense_id):
    return asset_controller.delete_expense(expense_id)
