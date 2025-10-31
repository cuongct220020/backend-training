from app.repositories.user_repository import UserRepository
from app.utils.security_utils import hash_password, verify_password, generate_jwt


async def register_user(user_repo: UserRepository, username: str, password: str, role: str = "member"):
    """Business logic for registering a new user."""
    # 1. Check if username exists by calling the repository
    existing_user = await user_repo.get_by_username(username)
    if existing_user:
        return {"error": "Username already exists"}

    # 2. Hash password
    hashed_pw = hash_password(password)

    # 3. Create user data and call the repository to create the user
    new_user_data = {
        "username": username,
        "password": hashed_pw,
        "user_role": role
    }
    new_user = await user_repo.create(new_user_data)
    await user_repo.session.flush()  # Flush to get the new user's ID

    return {"message": "User registered successfully", "user_id": new_user.id}


async def login_user(user_repo: UserRepository, username: str, password: str):
    """Business logic for user login."""
    # 1. Find user by username via repository
    user = await user_repo.get_by_username(username)

    # 2. Verify password
    if not user or not verify_password(password, user.password):
        return {"error": "Invalid username or password"}

    # 3. Generate and return an access token
    access_token = generate_jwt(subject=user.id)
    return {"message": "Login successful", "access_token": access_token, "token_type": "bearer"}
