from typing import Final

from app import create_app
from app.utils.logger_utils import get_logger
from config import Config, PostgreSQLConfig, DEFAULT_JWT_SECRET

logger = get_logger(__name__)

# Create the Sanic app instance as a module-level constant
app: Final = create_app(Config, PostgreSQLConfig)

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
    except (KeyError, OSError) as e:
        logger.error(f'Failed to start server: {e}')

if __name__ == '__main__':
    main()