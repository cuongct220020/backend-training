import os


class Config:
    RUN_SETTING = {
        'host': 'localhost',
        'port': 1337,
        'debug': True,
        "access_log": False,
        "auto_reload": True,
        'workers': 4
    }
    # uWSGI를 통해 배포되어야 하므로, production level에선 run setting을 건드리지 않음

    SECRET_KEY = os.getenv('SECRET_KEY', '85c145a16bd6f6e1f3e104ca78c6a102')


class LocalDBConfig:
    pass


class RemoteDBConfig:
    pass
