import os
from dotenv import load_dotenv

load_dotenv() # Load .env

# Default configuration
DEFAULT_APP_HOST = 'localhost'
DEFAULT_APP_PORT = 1337
DEFAULT_DEBUG_MODE = True
DEFAULT_WORKER_COUNT = 4

DEFAULT_JWT_SECRET = '85c145a16bd6f6e1f3e104ca78c6a102'
DEFAULT_JWT_ALGORITHM = 'HS256'
DEFAULT_JWT_EXPIRATION_MINUTES = 60

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
    JWT_ACCESS_TOKEN_EXPIRATION_SECONDS = os.getenv('JWT_ACCESS_TOKEN_EXPIRATION_MINUTES',
                                                    DEFAULT_JWT_EXPIRATION_MINUTES)

class PostgreSQLConfig:
    DB_TYPE = os.getenv('DB_TYPE')
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_NAME = os.getenv('DB_NAME')
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    DATABASE_URI = f'{DB_TYPE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

class RedisConfig:
    """Redis configuration."""
    REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
    REDIS_DB = int(os.getenv('REDIS_DB', 0))