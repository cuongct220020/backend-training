import os
from dotenv import load_dotenv
from sanic.response import text

from app import create_app
from app.apis import api
from app.misc.log import log
from config import Config, LocalDBConfig

# Load environment before anything else
load_dotenv()

# Create app at module-level (not inside __main__)
app = create_app(Config, LocalDBConfig)
app.blueprint(api)

@app.route("/hello-world")
async def hello_world(request):
    return text("Hello World")


# Check environment & log info
if not os.getenv("SECRET_KEY"):
    log(message="SECRET_KEY is not set in environment variables.", keyword="WARN")

log(message=f"Connecting to database: {LocalDBConfig.DATABASE_URI}", keyword="INFO")


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=1337,
        debug=True,
        access_log=True,
        auto_reload=True,
        workers=1
    )