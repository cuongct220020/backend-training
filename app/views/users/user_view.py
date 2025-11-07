from urllib.request import Request

from sanic.views import HTTPMethodView

class UserView(HTTPMethodView):
    async def get(self, request: Request):
        pass



