import os


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    _psycopg2_ok = False
    try:
        import psycopg2  # noqa: F401
        _psycopg2_ok = True
    except Exception:
        _psycopg2_ok = False
    db_user = os.getenv('DB_USER')
    if db_user and _psycopg2_ok:
        SQLALCHEMY_DATABASE_URI = (
            f"postgresql://{db_user}:{os.getenv('DB_PASSWORD')}"
            f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
        )
    else:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///cashflow.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    if db_user and _psycopg2_ok:
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
