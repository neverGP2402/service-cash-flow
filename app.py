import os
from flask import Flask
from dotenv import load_dotenv

load_dotenv()

from config.config import Config
from config.database import db, init_db
from config.jwt_config import jwt, init_jwt
from config.logger import init_logger, get_logger


def create_app():
    # Validate PostgreSQL configuration first
    try:
        # Check if psycopg2-binary is installed
        import psycopg2  # noqa: F401
    except ImportError:
        print("❌ Import Error: psycopg2-binary is required for PostgreSQL connection")
        print("💡 Solution: Install with 'pip install psycopg2-binary'")
        return None
    
    # Check if all required environment variables are set
    required_vars = ['DB_USER', 'DB_HOST', 'DB_PORT', 'DB_NAME', 'DB_PASSWORD']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"❌ Configuration Error: Missing required environment variables: {', '.join(missing_vars)}")
        print("💡 Solution: Check your .env file and ensure all PostgreSQL variables are set")
        return None
    
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Set database URI after validation
    db_user = os.getenv('DB_USER')
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT')
    db_name = os.getenv('DB_NAME')
    db_password = os.getenv('DB_PASSWORD')
    
    # URL encode password to handle special characters
    from urllib.parse import quote_plus
    encoded_password = quote_plus(db_password)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{db_user}:{encoded_password}@{db_host}:{db_port}/{db_name}"
    
    print(f"🚀 Starting {app.config.get('APP_NAME', 'Cash Flow Management')} v{app.config.get('APP_VERSION', '1.0.0')}")
    print(f"🌍 Environment: {'Development' if app.debug else 'Production'}")
    print(f"🔐 JWT Access Token Expires: {app.config.get('JWT_ACCESS_TOKEN_EXPIRES')}s")

    init_db(app)
    init_jwt(app)
    init_logger(app)

    # Configure CORS
    from flask_cors import CORS
    CORS(app, 
         origins=['http://localhost:3000', 'http://localhost:3039', 'http://172.25.240.50:3039', 'http://127.0.0.1:3000', 'http://127.0.0.1:3039', r'http://140\.245\.50\.242(:\d+)?'],
         methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
         allow_headers=['Content-Type', 'Authorization'],
         supports_credentials=True,
         max_age=86400)

    from flask_migrate import Migrate
    from config.database import db
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

    # Test database connection
    try:
        with app.app_context():
            from config.database import db
            db.create_all()
            print("✅ Database connected and tables created")
            print(f"📊 DB URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("💡 Solution: Install missing dependencies with 'pip install -r requirements.txt'")
        return None
    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
        print("💡 Solution: Check your .env file and ensure all required environment variables are set")
        return None
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("💡 Solution: Check your PostgreSQL server status and connection credentials")
        return None

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
    if app is None:
        print("❌ Application failed to start due to configuration errors")
        print("💡 Please fix the issues above and try again")
        exit(1)
    app.run(host='0.0.0.0', port=5000)
