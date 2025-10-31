from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.user import User
from app.utils.security_utils import hash_password, verify_password, generate_jwt


async def register_user(db_session: AsyncSession, username: str, password: str, role: str = "member"):
    """Registers a new user after validating data and hashing the password."""
    # Check if username exists
    result = await db_session.execute(select(User).where(User.username == username))
    if result.scalar_one_or_none():
        return {"error": "Username already exists"}

    # Hash password using the centralized security utility
    hashed_pw = hash_password(password)

    # Create new user instance
    new_user = User(
        username=username,
        password=hashed_pw,
        user_role=role
    )

    # Add to session and flush to get the ID
    db_session.add(new_user)
    await db_session.flush()

    return {"message": "User registered successfully", "user_id": new_user.id}


async def login_user(db_session: AsyncSession, username: str, password: str):
    """Handles user login, password verification, and JWT generation."""
    result = await db_session.execute(select(User).where(User.username == username))
    user = result.scalar_one_or_none()

    # Verify password using the centralized security utility
    if not user or not verify_password(password, user.password):
        return {"error": "Invalid username or password"}

    # Create and return an access token on successful login
    access_token = generate_jwt(subject=user.id)
    return {"message": "Login successful", "access_token": access_token, "token_type": "bearer"}
