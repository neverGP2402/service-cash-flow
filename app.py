import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

load_dotenv()

from config.config import Config
from config.database import db, init_db
from config.jwt_config import jwt, init_jwt
from config.logger import init_logger, get_logger


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    init_db(app)
    init_jwt(app)
    init_logger(app)

    Migrate(app, db)

    # Register blueprints
    from modules.auth.routes import auth_bp
    from modules.transaction.routes import transaction_bp
    from modules.debt.routes import debt_bp
    from modules.asset.routes import asset_bp
    from modules.report.routes import report_bp
    from modules.common_master.routes import common_master_bp

    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
    app.register_blueprint(transaction_bp, url_prefix='/api/v1/transaction')
    app.register_blueprint(debt_bp, url_prefix='/api/v1/debt')
    app.register_blueprint(asset_bp, url_prefix='/api/v1/asset')
    app.register_blueprint(report_bp, url_prefix='/api/v1/report')
    app.register_blueprint(common_master_bp, url_prefix='/api/v1/common')

    # Register middlewares
    from common.middlewares.auth_middleware import register_auth_middleware
    from common.middlewares.logging_middleware import register_logging_middleware
    from common.middlewares.request_middleware import register_request_middleware

    register_auth_middleware(app)
    register_logging_middleware(app)
    register_request_middleware(app)

    # Error handlers
    from common.exceptions.app_exception import register_error_handlers
    register_error_handlers(app)

    # Scheduler
    from jobs.scheduler import start_scheduler, shutdown_scheduler
    start_scheduler()

    @app.route('/health')
    def health():
        from datetime import datetime, timezone
        return {'status': 'ok', 'timestamp': datetime.now(timezone.utc).isoformat()}

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
