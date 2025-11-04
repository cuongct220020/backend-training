import pytest
from app import create_app

@pytest.fixture(scope="session")
def test_app():
    app = create_app()
    return app

@pytest.fixture
def test_client(test_app):
    return test_app.asgi_client
