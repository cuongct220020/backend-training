# app/service/auth_service
from datetime import datetime, UTC
from typing import cast

from app.constants.user_role_constants import UserRole
from app.extensions import redis_manager
from app.hooks import exceptions
from app.repositories.user_repository import UserRepository
from app.schemas.auth_schema import LoginSchema, Token
from app.schemas.user_schema import UserCreate, UserRead
from app.utils.security_utils import hash_password, verify_password, generate_jwt


async def register_user(user_repo: UserRepository, user_data: UserCreate) -> UserRead:
    """Business logic for registering a new user."""
    # 1. Check if username exists
    existing_user = await user_repo.get_by_username(user_data.username)
    if existing_user:
        raise exceptions.Conflict("Username already exists")

    # 2. Hash password
    hashed_pw = hash_password(user_data.password.get_secret_value())

    # 3. Create user data and call the repository
    new_user_data = {
        "username": user_data.username,
        "password": hashed_pw,
        "user_role": user_data.user_role.value
    }
    new_user = await user_repo.create(new_user_data)
    await user_repo.session.flush()  # Flush to get the new user's ID

    # 4. Return a clean DTO, not the ORM object
    return UserRead.model_validate(new_user)


async def login_user(user_repo: UserRepository, login_data: LoginSchema) -> Token:
    """Business logic for user login."""
    # 1. Find user by username
    user = await user_repo.get_by_username(login_data.username)

    # 2. Verify password. Use `cast` to inform the linter of the correct runtime type.
    if not user or not verify_password(
        login_data.password.get_secret_value(),
        cast(str, user.password)
    ):
        raise exceptions.Unauthorized("Invalid username or password")

    # 3. Generate and return an access token with the user's role
    token_payload = {"role": cast(UserRole, user.user_role).value}
    access_token = generate_jwt(
        subject=cast(int, user.user_id),
        extra_data=token_payload
    )
    
    return Token(access_token=access_token)


async def logout_user(jti: str, exp: int):
    """Adds a token's JTI to the deny-list until it expires."""
    now_ts = int(datetime.now(UTC).timestamp())
    # Calculate how many seconds the token has left to live
    # Add a small buffer (e.g., 5s) to account for clock skew
    remaining_time = exp - now_ts + 5

    if remaining_time > 0:
        await redis_manager.client.set(
            f"deny_list:jti:{jti}", "revoked", ex=remaining_time
        )
