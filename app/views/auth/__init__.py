#
# # ----- Xác minh token -----
# # Trường hợp sử dụng:
# # - Dùng trong Microservices, API Gateway xác minh token trước khi proxy đến service khác.
# # - SPA kiểm tra token trước khi render UI bảo mật.
# class VerifyToken(HTTPMethodView):
#     async def get(self, request: Request):
#         pass
#
# # Thu hồi token
# # Trường hợp sử dụng:
# # - Admin thu hồi token của user vi phạm.
# # - User hủy đăng nhập từ một thiết bị lạ.
# class RevokeToken(HTTPMethodView):
#     pass
