from sqlalchemy.future import select
from app.databases.postgresql import postgres_db
from app.models.user import User
from app.utils.security_utils import hash_password, verify_password, create_access_token


async def register_user(username: str, password: str, role: str = "member"):
    async with postgres_db.get_session() as session:
        # Check if username exists
        result = await session.execute(select(User).where(User.username == username))
        existing_user = result.scalar_one_or_none()
        if existing_user:
            return {"error": "Username already exists"}

        # Hash password using the centralized security utility
        hashed_pw = hash_password(password)

        # Create new user
        new_user = User(username=username, password=hashed_pw, user_role=role)
        session.add(new_user)
        await session.flush()
        await session.refresh(new_user)

        return {"message": "User registered successfully", "user_id": new_user.user_id}


async def login_user(username: str, password: str):
    async with postgres_db.get_session() as session:
        result = await session.execute(select(User).where(User.username == username))
        user = result.scalar_one_or_none()

        # Verify password using the centralized security utility
        if not user or not verify_password(password, user.password):
            return {"error": "Invalid username or password"}

        # Create and return an access token on successful login
        access_token = create_access_token(subject=user.user_id)
        return {"message": "Login successful", "access_token": access_token, "token_type": "bearer"}
