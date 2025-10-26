from tortoise import Tortoise

async def init_db(app):
    await Tortoise.init(
        db_url='postgres://postgres:postgres@localhost:5432/test',
        modules={'models': ['app.models']}
    )
    await Tortoise.generate_schemas()

    @app.listener('after_server_stop')
    async def cleanup(app, loop):
        await Tortoise.close_connections()