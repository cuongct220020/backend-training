import pytest

@pytest.mark.asyncio
async def test_create_user_api(test_client):
    payload = {"name": "Alice"}
    _, res = await test_client.post("/users", json=payload)
    assert res.status == 201
    data = res.json
    assert data["name"] == "Alice"
