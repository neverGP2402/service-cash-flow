from flask import Blueprint, request
from common.base.base_controller import BaseController
from common.middlewares.auth_middleware import jwt_required_custom, get_current_user_id
from common.exceptions.app_exception import BadRequestException
from modules.transaction.services.tran_transaction_service import TranTransactionService
from modules.transaction.services.tran_transaction_detail_service import TranTransactionDetailService
from modules.transaction.services.tran_notification_service import TranNotificationService
from modules.transaction.services.tran_accumulated_assets_time_line_service import TranAccumulatedAssetsTimeLineService
from modules.transaction.services.tran_accumulated_assets_by_date_service import TranAccumulatedAssetsByDateService
from modules.transaction.services.tran_result_by_month_service import TranResultByMonthService
from modules.transaction.models.tran_transactions import TranTransaction
from modules.transaction.models.tran_transactions_detail import TranTransactionDetail
from modules.transaction.models.tran_notification import TranNotification
from modules.transaction.models.tran_accumulated_assets_time_line import TranAccumulatedAssetsTimeLine
from modules.transaction.models.tran_accumulated_assets_by_date import TranAccumulatedAssetsByDate
from modules.transaction.models.tran_result_by_month import TranResultByMonth
from modules.transaction.validators.transaction_req import TransactionReq
from modules.transaction.validators.transaction_detail_req import TransactionDetailReq
from modules.transaction.validators.notification_req import NotificationReq

transaction_bp = Blueprint('transaction', __name__)


class TransactionController(BaseController):
    def __init__(self):
        self.transaction_service = TranTransactionService()
        self.detail_service = TranTransactionDetailService()
        self.notification_service = TranNotificationService()
        self.timeline_service = TranAccumulatedAssetsTimeLineService()
        self.by_date_service = TranAccumulatedAssetsByDateService()
        self.result_service = TranResultByMonthService()

    # Transaction endpoints
    def list_transactions(self):
        user_id = get_current_user_id()
        params = self._get_pagination_params()
        filters = self._get_filter_params(['type', 'category_id', 'status', 'wallet_id'])
        filters['user_id'] = user_id
        items = self.transaction_service.get_all(filters=filters, page=params['page'], limit=params['limit'])
        total = self.transaction_service.count(filters=filters)
        data = [i.to_dict() for i in items]
        return self.paginated(data=data, page=params['page'], limit=params['limit'], total=total)

    def get_transaction(self, transaction_id):
        item = self.transaction_service.get_by_id(transaction_id)
        if not item:
            return self.not_found('Transaction not found')
        return self.ok(data=item.to_dict())

    def create_transaction(self):
        data = request.get_json(force=True)
        if not data:
            raise BadRequestException('Request body is required')
        TransactionReq(data)
        user_id = get_current_user_id()
        entity = TranTransaction(
            user_id=user_id,
            type=data.get('type'),
            category_id=data.get('category_id'),
            bill_image=data.get('bill_image'),
            amount=data.get('amount', 0),
            date=data.get('date'),
            status=data.get('status', 'PENDING'),
            formality_transaction=data.get('formality_transaction'),
            wallet_id=data.get('wallet_id'),
            origin_transaction_id=data.get('origin_transaction_id'),
            description=data.get('description'),
            reference=data.get('reference'),
            meta_data=data.get('meta_data'),
            created_by_user_id=user_id,
            updated_by_user_id=user_id
        )
        created = self.transaction_service.create(entity)
        return self.created(data=created.to_dict())

    def update_transaction(self, transaction_id):
        data = request.get_json(force=True)
        if not data:
            raise BadRequestException('Request body is required')
        TransactionReq(data)
        entity = self.transaction_service.get_by_id(transaction_id)
        if not entity:
            return self.not_found('Transaction not found')
        for key, value in data.items():
            if hasattr(entity, key):
                setattr(entity, key, value)
        entity.updated_by_user_id = get_current_user_id()
        updated = self.transaction_service.update(entity)
        return self.ok(data=updated.to_dict())

    def delete_transaction(self, transaction_id):
        user_id = get_current_user_id()
        success = self.transaction_service.delete(transaction_id, deleted_by_user_id=user_id)
        if not success:
            return self.not_found('Transaction not found')
        return self.ok(message='Transaction deleted')

    # Transaction detail endpoints
    def list_details(self, transaction_id):
        items = self.detail_service.get_by_transaction_id(transaction_id)
        data = [i.to_dict() for i in items]
        return self.ok(data=data)

    def create_detail(self, transaction_id):
        data = request.get_json(force=True)
        TransactionDetailReq(data)
        user_id = get_current_user_id()
        entity = TranTransactionDetail(
            transaction_id=transaction_id,
            user_id=user_id,
            product_name=data.get('product_name'),
            amount=data.get('amount', 0),
            price=data.get('price', 0),
            into_money=data.get('into_money', 0),
            date=data.get('date'),
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

    # Notification endpoints
    def list_notifications(self):
        user_id = get_current_user_id()
        params = self._get_pagination_params()
        items = self.notification_service.get_by_user_id(user_id, params['page'], params['limit'])
        data = [i.to_dict() for i in items]
        return self.ok(data=data)

    def get_notification(self, notification_id):
        item = self.notification_service.get_by_id(notification_id)
        if not item:
            return self.not_found('Notification not found')
        return self.ok(data=item.to_dict())

    def create_notification(self):
        data = request.get_json(force=True)
        NotificationReq(data)
        user_id = get_current_user_id()
        entity = TranNotification(
            user_id=user_id,
            transaction_id=data.get('transaction_id'),
            title=data.get('title'),
            content=data.get('content'),
            type=data.get('type'),
            status=data.get('status'),
            sent_at=data.get('sent_at'),
            is_read=data.get('is_read', False),
            read_at=data.get('read_at'),
            priority=data.get('priority'),
            created_by_user_id=user_id,
            updated_by_user_id=user_id
        )
        created = self.notification_service.create(entity)
        return self.created(data=created.to_dict())

    def update_notification(self, notification_id):
        data = request.get_json(force=True)
        NotificationReq(data)
        entity = self.notification_service.get_by_id(notification_id)
        if not entity:
            return self.not_found('Notification not found')
        for key, value in data.items():
            if hasattr(entity, key):
                setattr(entity, key, value)
        entity.updated_by_user_id = get_current_user_id()
        updated = self.notification_service.update(entity)
        return self.ok(data=updated.to_dict())

    def delete_notification(self, notification_id):
        user_id = get_current_user_id()
        success = self.notification_service.delete(notification_id, deleted_by_user_id=user_id)
        if not success:
            return self.not_found('Notification not found')
        return self.ok(message='Notification deleted')


transaction_controller = TransactionController()


# Transaction routes
@transaction_bp.route('/transactions', methods=['GET'])
@jwt_required_custom
def list_transactions():
    return transaction_controller.list_transactions()


@transaction_bp.route('/transactions', methods=['POST'])
@jwt_required_custom
def create_transaction():
    return transaction_controller.create_transaction()


@transaction_bp.route('/transactions/<int:transaction_id>', methods=['GET'])
@jwt_required_custom
def get_transaction(transaction_id):
    return transaction_controller.get_transaction(transaction_id)


@transaction_bp.route('/transactions/<int:transaction_id>', methods=['PUT'])
@jwt_required_custom
def update_transaction(transaction_id):
    return transaction_controller.update_transaction(transaction_id)


@transaction_bp.route('/transactions/<int:transaction_id>', methods=['DELETE'])
@jwt_required_custom
def delete_transaction(transaction_id):
    return transaction_controller.delete_transaction(transaction_id)


# Transaction detail routes
@transaction_bp.route('/transactions/<int:transaction_id>/details', methods=['GET'])
@jwt_required_custom
def list_details(transaction_id):
    return transaction_controller.list_details(transaction_id)


@transaction_bp.route('/transactions/<int:transaction_id>/details', methods=['POST'])
@jwt_required_custom
def create_detail(transaction_id):
    return transaction_controller.create_detail(transaction_id)


@transaction_bp.route('/details/<int:detail_id>', methods=['DELETE'])
@jwt_required_custom
def delete_detail(detail_id):
    return transaction_controller.delete_detail(detail_id)


# Notification routes
@transaction_bp.route('/notifications', methods=['GET'])
@jwt_required_custom
def list_notifications():
    return transaction_controller.list_notifications()


@transaction_bp.route('/notifications', methods=['POST'])
@jwt_required_custom
def create_notification():
    return transaction_controller.create_notification()


@transaction_bp.route('/notifications/<int:notification_id>', methods=['GET'])
@jwt_required_custom
def get_notification(notification_id):
    return transaction_controller.get_notification(notification_id)


@transaction_bp.route('/notifications/<int:notification_id>', methods=['PUT'])
@jwt_required_custom
def update_notification(notification_id):
    return transaction_controller.update_notification(notification_id)


@transaction_bp.route('/notifications/<int:notification_id>', methods=['DELETE'])
@jwt_required_custom
def delete_notification(notification_id):
    return transaction_controller.delete_notification(notification_id)
