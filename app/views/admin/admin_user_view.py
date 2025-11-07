# app/views/admin/admin_user_view.py
from sanic.request import Request
from sanic.response import json
from sanic.views import HTTPMethodView
from sanic_ext import openapi
from sanic_ext.extensions.openapi.types import Schema

from app.decorators.auth import protected
from app.decorators.validate_request import validate_request
from app.repositories.user_repository import UserRepository
from app.repositories.user_session_repository import UserSessionRepository
from app.schemas.admin.user_admin_schema import AdminUserCreateSchema, AdminUserUpdateSchema, AdminUserResponseSchema
from app.schemas.response_schema import GenericResponse, PaginationResponse
from app.services.user_service import UserService


class AdminUserListView(HTTPMethodView):
    decorators = [protected(roles=["admin"])]

    @openapi.definition(
        summary="List all users (Admin only).",
        description="Retrieves a paginated list of all user accounts in the system.",
        response=Schema(PaginationResponse[AdminUserResponseSchema]),
        tag="Admin"
    )
    async def get(self, request: Request):
        """Lists all users with pagination."""
        user_repo = UserRepository(request.ctx.db_session)
        user_service = UserService(user_repo)

        try:
            page = int(request.args.get("page", 1))
            page_size = int(request.args.get("page_size", 10))
        except (ValueError, TypeError):
            page = 1
            page_size = 10

        paginated_result = await user_service.list_all_users(page=page, page_size=page_size)

        response = PaginationResponse(
            status="success",
            message="Users retrieved successfully.",
            data=paginated_result
        )
        return json(response.model_dump(by_alias=True), status=200)

    @openapi.definition(
        summary="Create a new user (Admin only).",
        description="Allows an admin to create a new user account with specified details.",
        body=Schema(AdminUserCreateSchema),
        response=Schema(GenericResponse[AdminUserResponseSchema]),
        tag="Admin"
    )
    @validate_request(AdminUserCreateSchema)
    async def post(self, request: Request):
        """Creates a new user account."""
        user_repo = UserRepository(request.ctx.db_session)
        user_service = UserService(user_repo)

        new_user = await user_service.create_user_by_admin(request.ctx.validated_data)

        response = GenericResponse(
            status="success",
            message="User created successfully.",
            data=AdminUserResponseSchema.model_validate(new_user)
        )
        return json(response.model_dump(by_alias=True), status=201)


class AdminUserDetailView(HTTPMethodView):
    decorators = [protected(roles=["admin"])]

    @openapi.definition(
        summary="Get user details by ID (Admin only).",
        description="Retrieves detailed information for a specific user account.",
        response=Schema(GenericResponse[AdminUserResponseSchema]),
        tag="Admin"
    )
    async def get(self, request: Request, user_id: int):
        """Retrieves details of a specific user."""
        user_repo = UserRepository(request.ctx.db_session)
        user_service = UserService(user_repo)

        user = await user_service.get_user_details_by_admin(user_id)

        response = GenericResponse(
            status="success",
            message="User details retrieved successfully.",
            data=AdminUserResponseSchema.model_validate(user)
        )
        return json(response.model_dump(by_alias=True), status=200)

    @openapi.definition(
        summary="Update user information by ID (Admin only).",
        description="Allows an admin to update specific fields of a user account.",
        body=Schema(AdminUserUpdateSchema),
        response=Schema(GenericResponse[AdminUserResponseSchema]),
        tag="Admin"
    )
    @validate_request(AdminUserUpdateSchema)
    async def patch(self, request: Request, user_id: int):
        """Updates information for a specific user."""
        user_repo = UserRepository(request.ctx.db_session)
        user_service = UserService(user_repo)

        updated_user = await user_service.update_user_by_admin(user_id, request.ctx.validated_data)

        response = GenericResponse(
            status="success",
            message="User updated successfully.",
            data=AdminUserResponseSchema.model_validate(updated_user)
        )
        return json(response.model_dump(by_alias=True), status=200)

    @openapi.definition(
        summary="Soft delete a user by ID (Admin only).",
        description="Deactivates a user account and revokes all their sessions.",
        response=Schema(GenericResponse),
        tag="Admin"
    )
    async def delete(self, request: Request, user_id: int):
        """Soft deletes a specific user and revokes their sessions."""
        user_repo = UserRepository(request.ctx.db_session)
        session_repo = UserSessionRepository(request.ctx.db_session)
        user_service = UserService(user_repo)

        await user_service.delete_user_by_admin(user_id, session_repo)

        response = GenericResponse(
            status="success",
            message="User deactivated and sessions revoked successfully."
        )
        return json(response.model_dump(), status=200)