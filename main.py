from typing import Final

from app import create_app
from app.utils.logger_utils import get_logger
from config import Config, PostgreSQLConfig, RedisConfig, EmailConfig, DEFAULT_JWT_SECRET

logger = get_logger(__name__)

# Create the Sanic app instance as a module-level constant
app: Final = create_app(Config, PostgreSQLConfig, RedisConfig, EmailConfig)

# Configure OpenAPI Security Schemes
app.config.OAS_SECURITY_SCHEMES = {
    "BearerAuth": {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT",
        "description": "JWT Authorization header using the Bearer scheme. Example: 'Authorization: Bearer {token}'"
    }
}

# Apply Security Scheme globally to all endpoints
app.config.OAS_SECURITY = [{"BearerAuth": []}]

def main() -> None:
    """Checks configuration and runs the application."""
    # Warn if the default secret key is being used in a non-debug environment
    if not app.config.get('DEBUG') and app.config.get('JWT_SECRET') == DEFAULT_JWT_SECRET:
        logger.warning(
            'JWT_SECRET is using the insecure default value in a production environment. '
            'Please set a strong secret key in your environment variables.'
        )

    try:
        app.run(**app.config['RUN_SETTING'])
    except (KeyError, OSError) as error:
        raise error

if __name__ == '__main__':
    main()