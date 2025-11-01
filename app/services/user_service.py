# app/services/user_service.py
from app.decorators.cache import cache
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserRead


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    # Apply the cache decorator
    # Cache the result for 5 minutes (300 seconds)
    # The result will be validated and parsed by the UserRead schema
    @cache(schema=UserRead, ttl=300, prefix="user_profile")
    async def get_user_by_id(self, user_id: int) -> User | None:
        """Fetches a user by their ID. The result of this function will be cached."""
        user = await self.user_repo.get_by_id(user_id)
        return user
