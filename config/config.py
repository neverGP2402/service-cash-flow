import os


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    
    # PostgreSQL configuration - will be validated in app.py
    SQLALCHEMY_DATABASE_URI = None  # Will be set in app.py after validation
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': int(os.getenv('DB_MIN_POOL', 3)),
        'max_overflow': int(os.getenv('DB_MAX_POOL', 10)) - int(os.getenv('DB_MIN_POOL', 3)),
        'pool_timeout': int(os.getenv('DB_CONNECTION_TIMEOUT', 30)),
    }

    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key')
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 3600))
    JWT_REFRESH_TOKEN_EXPIRES = int(os.getenv('JWT_REFRESH_TOKEN_EXPIRES', 604800))

    APP_NAME = os.getenv('APP_NAME', 'Cash Flow Management')
    APP_VERSION = os.getenv('APP_VERSION', '1.0.0')
