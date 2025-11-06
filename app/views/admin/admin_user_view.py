# app/views/admin/admin_user_view.py
from sanic.request import Request
from sanic.views import HTTPMethodView

class AdminUserView(HTTPMethodView):
    async def get(self, request: Request):
        pass
