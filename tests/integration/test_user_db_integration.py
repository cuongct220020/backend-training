import pytest
from app.models.user import User
from sqlalchemy import select

@pytest.mark.asyncio
async def test_create_and_query_user(db_session):
    new_user = User(name="Bob")
    db_session.add(new_user)
    await db_session.commit()

    result = await db_session.execute(select(User).where(User.name == "Bob"))
    user = result.scalar_one()
    assert user.name == "Bob"
