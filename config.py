import os
from dotenv import load_dotenv

# Load .env ngay đầu tiên
load_dotenv()

class Config:
    RUN_SETTING = {
        'host': os.getenv('APP_HOST', 'localhost'),
        'port': int(os.getenv('APP_PORT', 1337)),
        'debug': os.getenv('DEBUG', 'True').lower() == 'true',
        "access_log": False,
        "auto_reload": True,
        'workers': int(os.getenv('WORKERS', 4))
    }

    SECRET_KEY = os.getenv('SECRET_KEY', '85c145a16bd6f6e1f3e104ca78c6a102')
    DB_TYPE = os.getenv('DB_TYPE', 'postgresql')


class LocalDBConfig:
    @staticmethod
    def _get_database_uri():
        db_type = Config.DB_TYPE
        if db_type == 'postgresql':
            DB_USER = os.getenv('DB_USER')
            DB_PASSWORD = os.getenv('DB_PASSWORD')
            DB_NAME = os.getenv('DB_NAME')
            DB_HOST = os.getenv('DB_HOST')
            DB_PORT = os.getenv('DB_PORT')
            return f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
        elif db_type == 'sqlite':
            basedir = os.path.abspath(os.path.dirname(__file__))
            return 'sqlite:///' + os.path.join(basedir, 'app.db')
        raise ValueError(f"Unsupported DB_TYPE: {db_type}")

    DATABASE_URI = _get_database_uri()


class RemoteDBConfig:
    DB_USER = os.getenv('RDS_USERNAME')
    DB_PASSWORD = os.getenv('RDS_PASSWORD')
    DB_NAME = os.getenv('RDS_DB_NAME')
    DB_HOST = os.getenv('RDS_HOSTNAME')
    DB_PORT = os.getenv('RDS_PORT', 5432)
    DATABASE_URI = (
        f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?sslmode=require'
        if all([DB_USER, DB_PASSWORD, DB_HOST])
        else ''
    )
