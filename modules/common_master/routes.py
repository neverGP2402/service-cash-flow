from flask import Blueprint, request
from common.base.base_controller import BaseController
from common.middlewares.auth_middleware import jwt_required_custom, get_current_user_id
from common.exceptions.app_exception import BadRequestException
from modules.common_master.services.com_wallet_service import ComWalletService
from modules.common_master.services.com_asset_service import ComAssetService
from modules.common_master.services.com_origin_transaction_service import ComOriginTransactionService
from modules.common_master.services.com_exchange_rate_service import ComExchangeRateService
from modules.common_master.services.com_unit_service import ComUnitService
from modules.common_master.services.com_category_service import ComCategoryService
from modules.common_master.services.com_counterparty_service import ComCounterpartyService
from modules.common_master.models.com_wallets import ComWallet
from modules.common_master.models.com_asset import ComAsset
from modules.common_master.models.com_origin_transaction import ComOriginTransaction
from modules.common_master.models.com_exchange_rate import ComExchangeRate
from modules.common_master.models.com_unit import ComUnit
from modules.common_master.models.com_categories import ComCategory
from modules.common_master.models.com_counterparty import ComCounterparty
from modules.common_master.validators.wallet_req import WalletReq
from modules.common_master.validators.asset_req import AssetReq
from modules.common_master.validators.origin_req import OriginReq
from modules.common_master.validators.exchange_rate_req import ExchangeRateReq
from modules.common_master.validators.unit_req import UnitReq
from modules.common_master.validators.category_req import CategoryReq
from modules.common_master.validators.counterparty_req import CounterpartyReq

common_master_bp = Blueprint('common_master', __name__)


class CommonMasterController(BaseController):
    def __init__(self):
        self.wallet_service = ComWalletService()
        self.asset_service = ComAssetService()
        self.origin_service = ComOriginTransactionService()
        self.exchange_rate_service = ComExchangeRateService()
        self.unit_service = ComUnitService()
        self.category_service = ComCategoryService()
        self.counterparty_service = ComCounterpartyService()

    # Wallet
    def list_wallets(self):
        user_id = get_current_user_id()
        params = self._get_pagination_params()
        items = self.wallet_service.get_by_user_id(user_id, params['page'], params['limit'])
        data = [i.to_dict() for i in items]
        return self.ok(data=data)

    def create_wallet(self):
        data = request.get_json(force=True)
        if not data:
            raise BadRequestException('Request body is required')
        WalletReq(data)
        user_id = get_current_user_id()
        entity = ComWallet(
            user_id=user_id,
            code=data.get('code'),
            name=data.get('name'),
            type=data.get('type'),
            created_by_user_id=user_id,
            updated_by_user_id=user_id
        )
        created = self.wallet_service.create(entity)
        return self.created(data=created.to_dict())

    def get_wallet(self, wallet_id):
        item = self.wallet_service.get_by_id(wallet_id)
        if not item:
            return self.not_found('Wallet not found')
        return self.ok(data=item.to_dict())

    def update_wallet(self, wallet_id):
        data = request.get_json(force=True)
        if not data:
            raise BadRequestException('Request body is required')
        WalletReq(data)
        entity = self.wallet_service.get_by_id(wallet_id)
        if not entity:
            return self.not_found('Wallet not found')
        for key, value in data.items():
            if hasattr(entity, key):
                setattr(entity, key, value)
        entity.updated_by_user_id = get_current_user_id()
        updated = self.wallet_service.update(entity)
        return self.ok(data=updated.to_dict())

    def delete_wallet(self, wallet_id):
        user_id = get_current_user_id()
        success = self.wallet_service.delete(wallet_id, deleted_by_user_id=user_id)
        if not success:
            return self.not_found('Wallet not found')
        return self.ok(message='Wallet deleted')

    # Asset type
    def list_assets(self):
        params = self._get_pagination_params()
        items = self.asset_service.get_all(page=params['page'], limit=params['limit'])
        data = []
        for item in items:
            asset_dict = item.to_dict()
            # Thêm thông tin đơn vị
            if item.unit_id:
                unit = self.unit_service.get_by_id(item.unit_id)
                if unit:
                    asset_dict['unit_code'] = unit.code
                    asset_dict['unit_name'] = unit.name
            data.append(asset_dict)
        return self.ok(data=data)

    def create_asset(self):
        data = request.get_json(force=True)
        if not data:
            raise BadRequestException('Request body is required')
        AssetReq(data)
        user_id = get_current_user_id()
        entity = ComAsset(
            code=data.get('code'),
            name=data.get('name'),
            type=data.get('type'),
            unit_id=data.get('unit_id'),
            icon=data.get('icon'),
            created_by_user_id=user_id,
            updated_by_user_id=user_id
        )
        created = self.asset_service.create(entity)
        asset_dict = created.to_dict()
        # Thêm thông tin đơn vị
        if created.unit_id:
            unit = self.unit_service.get_by_id(created.unit_id)
            if unit:
                asset_dict['unit_code'] = unit.code
                asset_dict['unit_name'] = unit.name
        return self.created(data=asset_dict)

    def get_asset(self, asset_id):
        item = self.asset_service.get_by_id(asset_id)
        if not item:
            return self.not_found('Asset not found')
        
        asset_dict = item.to_dict()
        # Thêm thông tin đơn vị
        if item.unit_id:
            unit = self.unit_service.get_by_id(item.unit_id)
            if unit:
                asset_dict['unit_code'] = unit.code
                asset_dict['unit_name'] = unit.name
        return self.ok(data=asset_dict)

    def update_asset(self, asset_id):
        data = request.get_json(force=True)
        if not data:
            raise BadRequestException('Request body is required')
        AssetReq(data)
        entity = self.asset_service.get_by_id(asset_id)
        if not entity:
            return self.not_found('Asset not found')
        for key, value in data.items():
            if hasattr(entity, key):
                setattr(entity, key, value)
        entity.updated_by_user_id = get_current_user_id()
        updated = self.asset_service.update(entity)
        asset_dict = updated.to_dict()
        # Thêm thông tin đơn vị
        if updated.unit_id:
            unit = self.unit_service.get_by_id(updated.unit_id)
            if unit:
                asset_dict['unit_code'] = unit.code
                asset_dict['unit_name'] = unit.name
        return self.ok(data=asset_dict)

    def delete_asset(self, asset_id):
        user_id = get_current_user_id()
        success = self.asset_service.delete(asset_id, deleted_by_user_id=user_id)
        if not success:
            return self.not_found('Asset not found')
        return self.ok(message='Asset deleted')

    # Origin transaction
    def list_origins(self):
        params = self._get_pagination_params()
        items = self.origin_service.get_all(page=params['page'], limit=params['limit'])
        data = [i.to_dict() for i in items]
        return self.ok(data=data)

    def create_origin(self):
        data = request.get_json(force=True)
        if not data:
            raise BadRequestException('Request body is required')
        OriginReq(data)
        user_id = get_current_user_id()
        entity = ComOriginTransaction(
            code=data.get('code'),
            name=data.get('name'),
            created_by_user_id=user_id,
            updated_by_user_id=user_id
        )
        created = self.origin_service.create(entity)
        return self.created(data=created.to_dict())

    def get_origin(self, origin_id):
        item = self.origin_service.get_by_id(origin_id)
        if not item:
            return self.not_found('Origin not found')
        return self.ok(data=item.to_dict())

    def update_origin(self, origin_id):
        data = request.get_json(force=True)
        if not data:
            raise BadRequestException('Request body is required')
        OriginReq(data)
        entity = self.origin_service.get_by_id(origin_id)
        if not entity:
            return self.not_found('Origin not found')
        for key, value in data.items():
            if hasattr(entity, key):
                setattr(entity, key, value)
        entity.updated_by_user_id = get_current_user_id()
        updated = self.origin_service.update(entity)
        return self.ok(data=updated.to_dict())

    def delete_origin(self, origin_id):
        user_id = get_current_user_id()
        success = self.origin_service.delete(origin_id, deleted_by_user_id=user_id)
        if not success:
            return self.not_found('Origin not found')
        return self.ok(message='Origin deleted')

    # Exchange rate
    def list_exchange_rates(self):
        params = self._get_pagination_params()
        items = self.exchange_rate_service.get_all(page=params['page'], limit=params['limit'])
        data = [i.to_dict() for i in items]
        return self.ok(data=data)

    def create_exchange_rate(self):
        data = request.get_json(force=True)
        if not data:
            raise BadRequestException('Request body is required')
        ExchangeRateReq(data)
        user_id = get_current_user_id()
        entity = ComExchangeRate(
            exchange_rate_purchase=data.get('exchange_rate_purchase', 0),
            exchange_rate_sell=data.get('exchange_rate_sell', 0),
            asset_id=data.get('asset_id'),
            description=data.get('description'),
            origin_info=data.get('origin_info'),
            created_by_user_id=user_id,
            updated_by_user_id=user_id
        )
        created = self.exchange_rate_service.create(entity)
        return self.created(data=created.to_dict())

    def get_exchange_rate(self, rate_id):
        item = self.exchange_rate_service.get_by_id(rate_id)
        if not item:
            return self.not_found('Exchange rate not found')
        return self.ok(data=item.to_dict())

    def update_exchange_rate(self, rate_id):
        data = request.get_json(force=True)
        if not data:
            raise BadRequestException('Request body is required')
        ExchangeRateReq(data)
        entity = self.exchange_rate_service.get_by_id(rate_id)
        if not entity:
            return self.not_found('Exchange rate not found')
        for key, value in data.items():
            if hasattr(entity, key):
                setattr(entity, key, value)
        entity.updated_by_user_id = get_current_user_id()
        updated = self.exchange_rate_service.update(entity)
        return self.ok(data=updated.to_dict())

    def delete_exchange_rate(self, rate_id):
        user_id = get_current_user_id()
        success = self.exchange_rate_service.delete(rate_id, deleted_by_user_id=user_id)
        if not success:
            return self.not_found('Exchange rate not found')
        return self.ok(message='Exchange rate deleted')

    # Unit
    def list_units(self):
        params = self._get_pagination_params()
        items = self.unit_service.get_all(page=params['page'], limit=params['limit'])
        data = [i.to_dict() for i in items]
        return self.ok(data=data)

    def create_unit(self):
        data = request.get_json(force=True)
        if not data:
            raise BadRequestException('Request body is required')
        UnitReq(data)
        user_id = get_current_user_id()
        entity = ComUnit(
            code=data.get('code'),
            name=data.get('name'),
            created_by_user_id=user_id,
            updated_by_user_id=user_id
        )
        created = self.unit_service.create(entity)
        return self.created(data=created.to_dict())

    def get_unit(self, unit_id):
        item = self.unit_service.get_by_id(unit_id)
        if not item:
            return self.not_found('Unit not found')
        return self.ok(data=item.to_dict())

    def update_unit(self, unit_id):
        data = request.get_json(force=True)
        if not data:
            raise BadRequestException('Request body is required')
        UnitReq(data)
        entity = self.unit_service.get_by_id(unit_id)
        if not entity:
            return self.not_found('Unit not found')
        for key, value in data.items():
            if hasattr(entity, key):
                setattr(entity, key, value)
        entity.updated_by_user_id = get_current_user_id()
        updated = self.unit_service.update(entity)
        return self.ok(data=updated.to_dict())

    def delete_unit(self, unit_id):
        user_id = get_current_user_id()
        success = self.unit_service.delete(unit_id, deleted_by_user_id=user_id)
        if not success:
            return self.not_found('Unit not found')
        return self.ok(message='Unit deleted')

    # Category
    def list_categories(self):
        params = self._get_pagination_params()
        items = self.category_service.get_all(page=params['page'], limit=params['limit'])
        data = [i.to_dict() for i in items]
        return self.ok(data=data)

    def create_category(self):
        data = request.get_json(force=True)
        if not data:
            raise BadRequestException('Request body is required')
        CategoryReq(data)
        user_id = get_current_user_id()
        entity = ComCategory(
            code=data.get('code'),
            name=data.get('name'),
            type=data.get('type'),
            created_by_user_id=user_id,
            updated_by_user_id=user_id
        )
        created = self.category_service.create(entity)
        return self.created(data=created.to_dict())

    def get_category(self, category_id):
        item = self.category_service.get_by_id(category_id)
        if not item:
            return self.not_found('Category not found')
        return self.ok(data=item.to_dict())

    def update_category(self, category_id):
        data = request.get_json(force=True)
        if not data:
            raise BadRequestException('Request body is required')
        CategoryReq(data)
        entity = self.category_service.get_by_id(category_id)
        if not entity:
            return self.not_found('Category not found')
        for key, value in data.items():
            if hasattr(entity, key):
                setattr(entity, key, value)
        entity.updated_by_user_id = get_current_user_id()
        updated = self.category_service.update(entity)
        return self.ok(data=updated.to_dict())

    def delete_category(self, category_id):
        user_id = get_current_user_id()
        success = self.category_service.delete(category_id, deleted_by_user_id=user_id)
        if not success:
            return self.not_found('Category not found')
        return self.ok(message='Category deleted')

    # Counterparty
    def list_counterparties(self):
        params = self._get_pagination_params()
        items = self.counterparty_service.get_all(page=params['page'], limit=params['limit'])
        data = [i.to_dict() for i in items]
        return self.ok(data=data)

    def create_counterparty(self):
        data = request.get_json(force=True)
        if not data:
            raise BadRequestException('Request body is required')
        CounterpartyReq(data)
        user_id = get_current_user_id()
        entity = ComCounterparty(
            code=data.get('code'),
            name=data.get('name'),
            phone=data.get('phone'),
            avatar=data.get('avatar'),
            created_by_user_id=user_id,
            updated_by_user_id=user_id
        )
        created = self.counterparty_service.create(entity)
        return self.created(data=created.to_dict())

    def get_counterparty(self, counterparty_id):
        item = self.counterparty_service.get_by_id(counterparty_id)
        if not item:
            return self.not_found('Counterparty not found')
        return self.ok(data=item.to_dict())

    def update_counterparty(self, counterparty_id):
        data = request.get_json(force=True)
        if not data:
            raise BadRequestException('Request body is required')
        CounterpartyReq(data)
        entity = self.counterparty_service.get_by_id(counterparty_id)
        if not entity:
            return self.not_found('Counterparty not found')
        for key, value in data.items():
            if hasattr(entity, key):
                setattr(entity, key, value)
        entity.updated_by_user_id = get_current_user_id()
        updated = self.counterparty_service.update(entity)
        return self.ok(data=updated.to_dict())

    def delete_counterparty(self, counterparty_id):
        user_id = get_current_user_id()
        success = self.counterparty_service.delete(counterparty_id, deleted_by_user_id=user_id)
        if not success:
            return self.not_found('Counterparty not found')
        return self.ok(message='Counterparty deleted')


common_master_controller = CommonMasterController()


# Wallet routes
@common_master_bp.route('/wallets', methods=['GET'])
@jwt_required_custom
def list_wallets():
    return common_master_controller.list_wallets()


@common_master_bp.route('/wallets', methods=['POST'])
@jwt_required_custom
def create_wallet():
    return common_master_controller.create_wallet()


@common_master_bp.route('/wallets/<int:wallet_id>', methods=['GET'])
@jwt_required_custom
def get_wallet(wallet_id):
    return common_master_controller.get_wallet(wallet_id)


@common_master_bp.route('/wallets/<int:wallet_id>', methods=['PUT'])
@jwt_required_custom
def update_wallet(wallet_id):
    return common_master_controller.update_wallet(wallet_id)


@common_master_bp.route('/wallets/<int:wallet_id>', methods=['DELETE'])
@jwt_required_custom
def delete_wallet(wallet_id):
    return common_master_controller.delete_wallet(wallet_id)


# Asset type routes
@common_master_bp.route('/assets', methods=['GET'])
@jwt_required_custom
def list_assets():
    return common_master_controller.list_assets()


@common_master_bp.route('/assets', methods=['POST'])
@jwt_required_custom
def create_asset():
    return common_master_controller.create_asset()


@common_master_bp.route('/assets/<int:asset_id>', methods=['GET'])
@jwt_required_custom
def get_asset(asset_id):
    return common_master_controller.get_asset(asset_id)


@common_master_bp.route('/assets/<int:asset_id>', methods=['PUT'])
@jwt_required_custom
def update_asset(asset_id):
    return common_master_controller.update_asset(asset_id)


@common_master_bp.route('/assets/<int:asset_id>', methods=['DELETE'])
@jwt_required_custom
def delete_asset(asset_id):
    return common_master_controller.delete_asset(asset_id)


# Origin transaction routes
@common_master_bp.route('/origins', methods=['GET'])
@jwt_required_custom
def list_origins():
    return common_master_controller.list_origins()


@common_master_bp.route('/origins', methods=['POST'])
@jwt_required_custom
def create_origin():
    return common_master_controller.create_origin()


@common_master_bp.route('/origins/<int:origin_id>', methods=['GET'])
@jwt_required_custom
def get_origin(origin_id):
    return common_master_controller.get_origin(origin_id)


@common_master_bp.route('/origins/<int:origin_id>', methods=['PUT'])
@jwt_required_custom
def update_origin(origin_id):
    return common_master_controller.update_origin(origin_id)


@common_master_bp.route('/origins/<int:origin_id>', methods=['DELETE'])
@jwt_required_custom
def delete_origin(origin_id):
    return common_master_controller.delete_origin(origin_id)


# Exchange rate routes
@common_master_bp.route('/exchange-rates', methods=['GET'])
@jwt_required_custom
def list_exchange_rates():
    return common_master_controller.list_exchange_rates()


@common_master_bp.route('/exchange-rates', methods=['POST'])
@jwt_required_custom
def create_exchange_rate():
    return common_master_controller.create_exchange_rate()


@common_master_bp.route('/exchange-rates/<int:rate_id>', methods=['GET'])
@jwt_required_custom
def get_exchange_rate(rate_id):
    return common_master_controller.get_exchange_rate(rate_id)


@common_master_bp.route('/exchange-rates/<int:rate_id>', methods=['PUT'])
@jwt_required_custom
def update_exchange_rate(rate_id):
    return common_master_controller.update_exchange_rate(rate_id)


@common_master_bp.route('/exchange-rates/<int:rate_id>', methods=['DELETE'])
@jwt_required_custom
def delete_exchange_rate(rate_id):
    return common_master_controller.delete_exchange_rate(rate_id)


# Unit routes
@common_master_bp.route('/units', methods=['GET'])
@jwt_required_custom
def list_units():
    return common_master_controller.list_units()


@common_master_bp.route('/units', methods=['POST'])
@jwt_required_custom
def create_unit():
    return common_master_controller.create_unit()


@common_master_bp.route('/units/<int:unit_id>', methods=['GET'])
@jwt_required_custom
def get_unit(unit_id):
    return common_master_controller.get_unit(unit_id)


@common_master_bp.route('/units/<int:unit_id>', methods=['PUT'])
@jwt_required_custom
def update_unit(unit_id):
    return common_master_controller.update_unit(unit_id)


@common_master_bp.route('/units/<int:unit_id>', methods=['DELETE'])
@jwt_required_custom
def delete_unit(unit_id):
    return common_master_controller.delete_unit(unit_id)


# Category routes
@common_master_bp.route('/categories', methods=['GET'])
@jwt_required_custom
def list_categories():
    return common_master_controller.list_categories()


@common_master_bp.route('/categories', methods=['POST'])
@jwt_required_custom
def create_category():
    return common_master_controller.create_category()


@common_master_bp.route('/categories/<int:category_id>', methods=['GET'])
@jwt_required_custom
def get_category(category_id):
    return common_master_controller.get_category(category_id)


@common_master_bp.route('/categories/<int:category_id>', methods=['PUT'])
@jwt_required_custom
def update_category(category_id):
    return common_master_controller.update_category(category_id)


@common_master_bp.route('/categories/<int:category_id>', methods=['DELETE'])
@jwt_required_custom
def delete_category(category_id):
    return common_master_controller.delete_category(category_id)


# Counterparty routes
@common_master_bp.route('/counterparties', methods=['GET'])
@jwt_required_custom
def list_counterparties():
    return common_master_controller.list_counterparties()


@common_master_bp.route('/counterparties', methods=['POST'])
@jwt_required_custom
def create_counterparty():
    return common_master_controller.create_counterparty()


@common_master_bp.route('/counterparties/<int:counterparty_id>', methods=['GET'])
@jwt_required_custom
def get_counterparty(counterparty_id):
    return common_master_controller.get_counterparty(counterparty_id)


@common_master_bp.route('/counterparties/<int:counterparty_id>', methods=['PUT'])
@jwt_required_custom
def update_counterparty(counterparty_id):
    return common_master_controller.update_counterparty(counterparty_id)


@common_master_bp.route('/counterparties/<int:counterparty_id>', methods=['DELETE'])
@jwt_required_custom
def delete_counterparty(counterparty_id):
    return common_master_controller.delete_counterparty(counterparty_id)
