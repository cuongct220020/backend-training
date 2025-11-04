import pytest
from app.models.user import User
from tests.mocks.mock_user_repo import MockUserRepo

@pytest.mark.asyncio
async def test_add_user_to_repo():
    repo = MockUserRepo()
    user = User(id=1, name="Alice")
    await repo.add(user)
    users = await repo.list()
    assert len(users) == 1
    assert users[0].name == "Alice"