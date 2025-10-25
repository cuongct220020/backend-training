from sanic import Blueprint

from app.apis.example_blueprint import example

api = Blueprint.group([example])
