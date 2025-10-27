from typing import Final

from app import create_app
from app.misc.log import log
from config import Config, PostgreSQLConfig, DEFAULT_SECRET_KEY

# Create the Sanic app instance as a module-level constant
app: Final = create_app(Config, PostgreSQLConfig)

def main() -> None:
    """Checks configuration and runs the application."""
    # Warn if the default secret key is being used in a non-debug environment
    if not app.config.get('DEBUG') and app.config.get('SECRET_KEY') == DEFAULT_SECRET_KEY:
        log(
            message='SECRET_KEY is using the insecure default value in a production environment. ' \
                    'Please set a strong secret key in your environment variables.',
            keyword='WARN'
        )

    try:
        app.run(**app.config['RUN_SETTING'])
    except (KeyError, OSError) as e:
        log(f'Failed to start server: {e}', keyword='ERROR')

if __name__ == '__main__':
    main()