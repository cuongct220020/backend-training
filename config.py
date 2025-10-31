import os
from dotenv import load_dotenv

load_dotenv() # Load .env

DEFAULT_JWT_SECRET = '85c145a16bd6f6e1f3e104ca78c6a102'

class Config:
    RUN_SETTING = {
        'host': os.getenv('APP_HOST', 'localhost'),
        'port': int(os.getenv('APP_PORT', 1337)),
        'debug': os.getenv('DEBUG', 'True').lower() == 'true',
        "access_log": False,
        "auto_reload": True,
        'workers': int(os.getenv('WORKERS', 4))
    }

    JWT_SECRET = os.getenv('JWT_SECRET', DEFAULT_JWT_SECRET)

class PostgreSQLConfig:
    DB_TYPE = os.getenv('DB_TYPE')
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_NAME = os.getenv('DB_NAME')
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    DATABASE_URI = f'{DB_TYPE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

class RedisConfig:
    pass