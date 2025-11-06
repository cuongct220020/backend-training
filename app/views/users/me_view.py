# app/views/users/me_view.py
from sanic.request import Request
from sanic.views import HTTPMethodView

class MeView(HTTPMethodView):
    async def get(self, request: Request):
        pass