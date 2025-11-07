import os
from dotenv import load_dotenv

load_dotenv() # Load .env

# Default configuration
DEFAULT_APP_HOST = 'localhost'
DEFAULT_APP_PORT = 1337
DEFAULT_DEBUG_MODE = True
DEFAULT_WORKER_COUNT = 2

DEFAULT_JWT_SECRET = '85c145a16bd6f6e1f3e104ca78c6a102'
DEFAULT_JWT_ALGORITHM = 'HS256'
DEFAULT_JWT_EXPIRATION_MINUTES = 10

DEFAULT_REFRESH_TOKEN_EXPIRE_DAYS = 7

class Config:
    RUN_SETTING = {
        'host': os.getenv('APP_HOST', DEFAULT_APP_HOST),
        'port': int(os.getenv('APP_PORT', DEFAULT_APP_HOST)),
        'debug': os.getenv('DEBUG', DEFAULT_DEBUG_MODE).lower() == 'true',
        "access_log": False,
        "auto_reload": True,
        'workers': int(os.getenv('WORKERS', DEFAULT_WORKER_COUNT)),
    }

    JWT_SECRET = os.getenv('JWT_SECRET', DEFAULT_JWT_SECRET)
    JWT_ALGORITHM = os.getenv('JWT_ALGORITHM', DEFAULT_JWT_ALGORITHM)
    JWT_EXPIRATION_MINUTES = os.getenv('JWT_EXPIRATION_MINUTES', DEFAULT_JWT_EXPIRATION_MINUTES)

    REFRESH_TOKEN_EXPIRE_DAYS = os.getenv('REFRESH_TOKEN_EXPIRE_DAYS', DEFAULT_REFRESH_TOKEN_EXPIRE_DAYS)

class PostgreSQLConfig:
    DB_DRIVER = os.getenv('DB_DRIVER')
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_NAME = os.getenv('DB_NAME')
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    DATABASE_URI = f'{DB_DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

class RedisConfig:
    """Redis configuration."""
    REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
    REDIS_DB = int(os.getenv('REDIS_DB', 0))

class EmailConfig:
    # Email server configuration (for Gmail)
    EMAIL_HOST = "smtp.gmail.com"
    EMAIL_PORT = 587  # Port for TLS
    EMAIL_SENDER = os.getenv("EMAIL_SENDER")  # Your Gmail address, e.g., "your.email@gmail.com"
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")  # The 16-character App Password you generated