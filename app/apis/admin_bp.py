# app/apis/admin_bp.py
from sanic import Blueprint
from app.views.admin.admin_user_view import AdminUserView

admin_bp = Blueprint('admin', url_prefix='/admin')

admin_bp.add_route(AdminUserView.as_view(), '/admin/user')