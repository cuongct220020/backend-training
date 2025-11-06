from sanic import Request
from sanic.views import HTTPMethodView

# ----- Mở khoá tài khoản -----
class UnlockView(HTTPMethodView):
    async def get(self, request: Request):
        pass