import pytest
from httpx import AsyncClient

from main import app


@pytest.mark.asyncio
async def test_register_and_login():
    async with AsyncClient(app=app, base_url='http://test') as ac:
        payload = {"username": "testuser", "email": "t@example.com", "password": "secret"}
        r = await ac.post('/auth/register', json=payload)
        assert r.status_code == 201
        body = r.json()
        assert body['username'] == 'testuser'

        r2 = await ac.post('/auth/login', json={"username": "testuser", "password": "secret"})
        assert r2.status_code == 200
        assert 'access_token' in r2.json()
