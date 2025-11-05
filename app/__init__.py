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
    from app.hooks.caching import setup_redis, close_redis

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
    from app.hooks.database import manage_db_session
    from app.hooks.caching import inject_redis_client
    from app.hooks.request_auth import auth

    # IMPORTANT: The order of middleware can be important.
    # Middlewares that wrap the handler are executed like onion layers.

    # 1. (Outermost) Measures and logs response time
    sanic_app.register_middleware(add_start_time, attach_to='request')
    sanic_app.register_middleware(add_spent_time, attach_to='response')

    # 2. Manages DB session lifecycle (commit, rollback, close)
    # This should wrap the business logic to ensure transactions are handled correctly.
    sanic_app.register_middleware(manage_db_session)

    # 3. Injects Redis client into the request context
    sanic_app.register_middleware(inject_redis_client, attach_to='request')

    # 4. Authentication middleware
    sanic_app.register_middleware(auth, attach_to='request')

    # 5. (Innermost) Generic post-request hook
    sanic_app.register_middleware(after_request, attach_to='response')



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
