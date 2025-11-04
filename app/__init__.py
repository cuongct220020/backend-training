# app/__init__.py
from sanic import Sanic
from sanic_cors import CORS

from app.utils.logger_utils import get_logger

logger = get_logger(__name__)

def register_extensions(sanic_app: Sanic):
    from app import extensions

    extensions.cors = CORS(sanic_app,resources={r"/*": {"origins": "*"}})


def register_listeners(sanic_app: Sanic):
    from app.hooks.database import setup_db, close_db
    from app.hooks.redis import setup_redis, close_redis

    # Register database hooks
    sanic_app.register_listener(setup_db, "before_server_start")
    sanic_app.register_listener(close_db, "after_server_stop")

    # Register Redis hooks
    sanic_app.register_listener(setup_redis, "before_server_start")
    sanic_app.register_listener(close_redis, "after_server_stop")

def register_views(sanic_app: Sanic):
    from app.apis import api # Import the api Blueprint.group

    # Register the main API blueprint group with the /api/v1 prefix
    sanic_app.blueprint(api, url_prefix="/api/v1")

def register_hooks(sanic_app: Sanic):
    from app.hooks.request_context import after_request
    from app.hooks.response_time import add_start_time, add_spent_time
    from app.hooks.database import acquire_db_session, release_db_session
    from app.hooks.request_auth import auth

    sanic_app.register_middleware(after_request, attach_to='response')

    # Session per-request
    sanic_app.register_middleware(acquire_db_session, attach_to='request')
    sanic_app.register_middleware(release_db_session, attach_to='response')

    # Calculate response time
    sanic_app.register_middleware(add_start_time, attach_to='request')
    sanic_app.register_middleware(add_spent_time, attach_to='response')

    # Authentication
    sanic_app.register_middleware(auth, attach_to='request')


def register_error_handlers(sanic_app: Sanic):
    """Imports and registers all custom error handlers for the application."""
    from app.hooks.error_handler import register_error_handlers as register
    register(sanic_app)


def create_app(*config_cls) -> Sanic:
    logger.info(f"Sanic application initialized with { ', '.join([config.__name__ for config in config_cls]) }")

    sanic_app = Sanic(__name__)

    for config in config_cls:
        sanic_app.update_config(config)

    register_extensions(sanic_app)
    register_listeners(sanic_app)
    register_views(sanic_app)
    register_hooks(sanic_app)
    register_error_handlers(sanic_app)

    return sanic_app
